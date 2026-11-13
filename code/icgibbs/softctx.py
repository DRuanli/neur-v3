"""softctx.py — ngữ cảnh nhãn MỀM cho TabICL v2 (bài v3, 13/11/2026).

Ý tưởng: TabICL mã hoá nhãn của các điểm trong ngữ cảnh bằng `OneHotAndLinear`, tức Linear(one_hot(y)), ở hai chỗ:
phần nhúng cột (col_target_aware) và phần học trong ngữ cảnh. Thay one_hot(y_i) bằng một vector xác suất q_i thì
embedding là tổ hợp lồi của các embedding lớp; với q_i one-hot, mô hình giữ nguyên hoàn toàn.

Hai cách dùng:
  * `soft_labels(Q)`: context manager. Trong khối `with`, mọi lời gọi OneHotAndLinear trên nhãn của T điểm ngữ cảnh
    dùng ma trận Q (T × C) thay cho nhãn nguyên. Nhãn nguyên vẫn được truyền vào cho phần bookkeeping
    (`dummy_labels(Q)` bảo đảm đủ C lớp xuất hiện).
  * `SoftContextTabICL`: bọc TabICLClassifier, tắt hoán vị lớp (class_shuffle_method='none') để Q khớp chỉ số lớp.

Giới hạn hiện tại: C <= max_classes của checkpoint (10 với TabICL v2); không dùng phân lớp phân cấp.
Bản vá chỉ áp lên lớp OneHotAndLinear trong khối `with` và luôn được gỡ khi ra khỏi khối, kể cả khi có lỗi.
"""
from __future__ import annotations

import contextlib
import threading

import numpy as np
import torch
import torch.nn.functional as F

_LOCK = threading.Lock()
_STATE = {"Q": None, "calls": 0}


class SoftContextError(RuntimeError):
    pass


def _soft_forward_factory(orig):
    def forward(self, src):
        Q = _STATE["Q"]
        if Q is None:
            return orig(self, src)
        T = Q.shape[0]
        if src.shape[-1] != T:
            raise SoftContextError(
                f"OneHotAndLinear nhận {src.shape[-1]} nhãn nhưng Q có {T} dòng: mô hình đã lấy mẫu con hay sắp xếp lại "
                "ngữ cảnh, nên Q không còn khớp từng điểm")
        if Q.shape[1] > self.num_classes:
            raise SoftContextError(f"Q có {Q.shape[1]} lớp, encoder chỉ có {self.num_classes}")
        q = Q.to(device=self.weight.device, dtype=self.weight.dtype)
        if q.shape[1] < self.num_classes:
            q = F.pad(q, (0, self.num_classes - q.shape[1]))
        emb = F.linear(q, self.weight, self.bias)                       # (T, E)
        _STATE["calls"] += 1
        return emb.expand(*src.shape[:-1], T, emb.shape[-1])
    return forward


@contextlib.contextmanager
def soft_labels(Q):
    """Trong khối này, nhãn của T điểm ngữ cảnh là các hàng của Q (T × C, mỗi hàng là một phân phối)."""
    from tabicl._model.layers import OneHotAndLinear
    Q = torch.as_tensor(np.asarray(Q, dtype=np.float32))
    if Q.ndim != 2 or not torch.isfinite(Q).all() or (Q < 0).any():
        raise ValueError("Q phải là ma trận T × C không âm, hữu hạn")
    if not torch.allclose(Q.sum(1), torch.ones(Q.shape[0]), atol=1e-4):
        raise ValueError("mỗi hàng của Q phải có tổng bằng 1")
    with _LOCK:
        orig = OneHotAndLinear.forward
        OneHotAndLinear.forward = _soft_forward_factory(orig)
        _STATE["Q"], _STATE["calls"] = Q, 0
        try:
            yield _STATE
        finally:
            OneHotAndLinear.forward = orig
            _STATE["Q"] = None


def dummy_labels(Q):
    """Nhãn nguyên cho phần bookkeeping của TabICL: argmax của Q, rồi sửa để mọi lớp đều xuất hiện ít nhất một lần.
    Nhãn này KHÔNG đi vào embedding trong khối `soft_labels`."""
    Q = np.asarray(Q)
    y = Q.argmax(1).copy()
    C = Q.shape[1]
    taken = set()
    for k in range(C):
        if (y == k).sum() == 0:
            order = np.argsort(-Q[:, k])
            for i in order:
                if i not in taken and (y == y[i]).sum() > 1:
                    y[i] = k
                    taken.add(int(i))
                    break
    if len(np.unique(y)) < C:
        raise SoftContextError("không gán được đủ C lớp cho nhãn bookkeeping (quá ít điểm)")
    return y


def normalize_rows(M, eps=1e-12):
    M = np.clip(np.asarray(M, dtype=np.float64), 0, None)
    s = M.sum(1, keepdims=True)
    out = np.where(s > eps, M / np.maximum(s, eps), 1.0 / M.shape[1])
    return out


class SoftContextTabICL:
    """TabICL với ngữ cảnh nhãn mềm. `clf_kwargs` chuyển cho TabICLClassifier (ví dụ model_path, n_estimators, device).
    Hoán vị lớp bị tắt để chỉ số cột của Q khớp chỉ số lớp."""

    def __init__(self, **clf_kwargs):
        clf_kwargs = dict(clf_kwargs)
        if clf_kwargs.get("class_shuffle_method", "none") != "none":
            raise ValueError("SoftContextTabICL cần class_shuffle_method='none'")
        clf_kwargs["class_shuffle_method"] = "none"
        self.clf_kwargs = clf_kwargs

    def predict_proba(self, X_ctx, Q_ctx, X_query):
        from tabicl import TabICLClassifier
        Q_ctx = normalize_rows(Q_ctx)
        y = dummy_labels(Q_ctx)
        clf = TabICLClassifier(**self.clf_kwargs)
        with soft_labels(Q_ctx) as st:
            clf.fit(np.asarray(X_ctx), y)
            P = clf.predict_proba(np.asarray(X_query))
            if st["calls"] == 0:
                raise SoftContextError("không có lời gọi nào tới encoder nhãn: bản vá không có tác dụng")
        return np.asarray(P, dtype=np.float64)


def mean_field(predictor, X, L, X_test=None, n_iter=5, n_folds=5, damping=0.5, rng=None, Q0=None, callback=None):
    """Suy luận trường trung bình trong ngữ cảnh (In-Context Mean-Field).

    L: ma trận hệ số hợp lý của nhãn yếu (n × C), L[i, k] ∝ P(nhãn yếu của i | y_i = k). Q0 mặc định = chuẩn hoá L.
    Mỗi vòng: chia n điểm thành `n_folds` phần; với mỗi phần, ngữ cảnh là các phần còn lại với nhãn mềm Q, dự đoán
    P_i cho các điểm của phần đó; rồi Q_i <- (1 − damping)·chuẩn hoá(L_i ⊙ P_i) + damping·Q_i.
    Trả về (Q, P_test) với P_test là dự đoán cho X_test khi ngữ cảnh là toàn bộ n điểm với nhãn mềm Q cuối.
    """
    rng = np.random.default_rng(rng)
    L = np.asarray(L, dtype=np.float64)
    n = len(L)
    Q = normalize_rows(L) if Q0 is None else normalize_rows(Q0)
    for t in range(n_iter):
        folds = np.array_split(rng.permutation(n), n_folds)
        P = np.empty_like(Q)
        for f in folds:
            ctx = np.setdiff1d(np.arange(n), f)
            P[f] = predictor.predict_proba(X[ctx], Q[ctx], X[f])
        Q = (1 - damping) * normalize_rows(L * P) + damping * Q
        if callback is not None:
            callback(t, Q)
    P_test = predictor.predict_proba(X, Q, X_test) if X_test is not None else None
    return Q, P_test
