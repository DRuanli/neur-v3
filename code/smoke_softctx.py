"""smoke_softctx.py — lượt kiểm KỸ THUẬT cho ngữ cảnh nhãn mềm với trọng số TabICL v2 thật (bài v3, mốc A0).

Đây KHÔNG phải thí nghiệm: không đo chất lượng của SCI, không in độ chính xác của phương pháp nào, để không nhìn trước
kết quả của thí điểm A1. Chỉ kiểm:
  K1  dự đoán với nhãn mềm one-hot trùng dự đoán với nhãn cứng (sai lệch tuyệt đối lớn nhất);
  K2  nhãn mềm khác one-hot thì dự đoán đổi (bản vá có tác dụng);
  K3  không có lỗi lệch hàng khi ngữ cảnh 500, 1.000, 2.000, 5.000 điểm (TabICL không tự lấy mẫu con hay đảo hàng);
  K4  thời gian một lần gọi theo cỡ ngữ cảnh, và thời gian một vòng trường trung bình; bộ nhớ GPU lớn nhất.
Dữ liệu: dataset có sẵn trong scikit-learn (wine, breast_cancer) và dữ liệu tổng hợp make_classification; không cần OpenML.

Chạy: python smoke_softctx.py --out /kaggle/working [--device cuda] [--model_path ĐƯỜNG_DẪN]   (từ thư mục code/)
"""
import argparse
import json
import os
import time

import numpy as np


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".")
    ap.add_argument("--device", default=None)
    ap.add_argument("--model_path", default=None, help="checkpoint cục bộ (để thử trên CPU); mặc định tải TabICL v2")
    ap.add_argument("--sizes", default="500,1000,2000,5000")
    ap.add_argument("--n_estimators", type=int, default=8)
    a = ap.parse_args(argv)
    import torch
    from sklearn.datasets import load_breast_cancer, load_wine, make_classification
    from icgibbs import softctx as sc

    dev = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    kw = dict(device=dev, n_estimators=a.n_estimators, random_state=0)
    if a.model_path:
        kw.update(model_path=a.model_path, allow_auto_download=False)
    rep = {"device": dev, "torch": torch.__version__, "n_estimators": a.n_estimators,
           "gpu": torch.cuda.get_device_name(0) if dev == "cuda" else None, "checks": {}}
    if dev == "cuda":
        torch.cuda.reset_peak_memory_stats()

    def hard_vs_soft(X, y, n_ctx):
        from tabicl import TabICLClassifier
        C = int(y.max()) + 1
        h = TabICLClassifier(class_shuffle_method="none", **kw).fit(X[:n_ctx], y[:n_ctx]).predict_proba(X[n_ctx:])
        s = sc.SoftContextTabICL(**kw).predict_proba(X[:n_ctx], np.eye(C)[y[:n_ctx]], X[n_ctx:])
        u = sc.SoftContextTabICL(**kw).predict_proba(X[:n_ctx], np.full((n_ctx, C), 1.0 / C), X[n_ctx:])
        return float(np.abs(h - s).max()), float(np.abs(s - u).max())

    for name, (X, y) in {"wine": load_wine(return_X_y=True), "breast_cancer": load_breast_cancer(return_X_y=True)}.items():
        X = X.astype(np.float32)
        rng = np.random.default_rng(0)
        idx = rng.permutation(len(y))
        X, y = X[idx], y[idx]
        n_ctx = int(0.7 * len(y))
        d_onehot, d_uniform = hard_vs_soft(X, y, n_ctx)
        rep["checks"][f"K1_{name}"] = {"max_abs_diff_hard_vs_onehot_soft": d_onehot, "pass": d_onehot < 1e-3}
        rep["checks"][f"K2_{name}"] = {"max_abs_diff_onehot_vs_uniform": d_uniform, "pass": d_uniform > 1e-3}

    timing = {}
    for n in [int(s) for s in a.sizes.split(",")]:
        X, y = make_classification(n_samples=n + 500, n_features=20, n_informative=8, n_classes=5, random_state=0)
        X = X.astype(np.float32)
        Q = sc.normalize_rows(np.random.default_rng(1).random((n, 5)) + np.eye(5)[y[:n]] * 2)
        m = sc.SoftContextTabICL(**kw)
        try:
            t0 = time.time()
            P = m.predict_proba(X[:n], Q, X[n:])
            timing[n] = {"seconds": round(time.time() - t0, 2), "ok": bool(np.allclose(P.sum(1), 1, atol=1e-4))}
        except sc.SoftContextError as e:
            timing[n] = {"error": str(e)[:300]}
    rep["checks"]["K3_K4_context_sizes"] = timing

    X, y = make_classification(n_samples=1500, n_features=20, n_informative=8, n_classes=5, random_state=1)
    X = X.astype(np.float32)
    rng = np.random.default_rng(2)
    L = (rng.random((1000, 5)) < 0.6).astype(float)
    L[np.arange(1000), y[:1000]] = 1.0
    t0 = time.time()
    Q, P = sc.mean_field(sc.SoftContextTabICL(**kw), X[:1000], L, X_test=X[1000:], n_iter=1, n_folds=10, rng=0)
    rep["checks"]["K4_mean_field_one_iter_n1000"] = {"seconds": round(time.time() - t0, 2),
                                                     "respects_candidates": bool(np.all(Q[L == 0] < 1e-9))}
    if dev == "cuda":
        rep["gpu_peak_mem_gb"] = round(torch.cuda.max_memory_allocated() / 2 ** 30, 2)
    rep["all_pass"] = all(v.get("pass", True) for k, v in rep["checks"].items() if k.startswith(("K1", "K2"))) and \
        all("error" not in v for v in timing.values())
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "v3_SMOKE_report.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print(json.dumps(rep, indent=1))
    return 0 if rep["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
