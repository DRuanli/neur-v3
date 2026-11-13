"""Test cho icgibbs.softctx (ngữ cảnh nhãn mềm cho TabICL). Dùng một checkpoint TabICL nhỏ khởi tạo ngẫu nhiên trên CPU,
vì môi trường kiểm thử không tải được trọng số thật; các test chỉ kiểm tính đúng của đường đưa nhãn mềm, không kiểm chất lượng."""
import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("tabicl")

from icgibbs import softctx as sc  # noqa: E402

SMALL = dict(max_classes=10, embed_dim=16, col_num_blocks=1, col_nhead=2, col_num_inds=8, row_num_blocks=1, row_nhead=2,
             row_num_cls=2, icl_num_blocks=2, icl_nhead=2, zero_init=False)


@pytest.fixture(scope="module")
def ckpt(tmp_path_factory):
    from tabicl._model.tabicl import TabICL
    torch.manual_seed(0)
    m = TabICL(**SMALL)
    p = tmp_path_factory.mktemp("ck") / "tiny.ckpt"
    torch.save({"config": SMALL, "state_dict": m.state_dict()}, p)
    return str(p)


@pytest.fixture(scope="module")
def data():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((90, 5)).astype(np.float32)
    y = (X[:, 0] > 0).astype(int) + (X[:, 1] > 0.5).astype(int)          # 3 lớp
    return X, y


def kw(ckpt):
    return dict(model_path=ckpt, n_estimators=2, device="cpu", allow_auto_download=False, random_state=0)


def test_onehot_soft_equals_hard(ckpt, data):
    from tabicl import TabICLClassifier
    X, y = data
    hard = TabICLClassifier(class_shuffle_method="none", **kw(ckpt)).fit(X[:60], y[:60]).predict_proba(X[60:])
    soft = sc.SoftContextTabICL(**kw(ckpt)).predict_proba(X[:60], np.eye(3)[y[:60]], X[60:])
    assert np.allclose(hard, soft, atol=1e-5)


def test_soft_labels_change_predictions(ckpt, data):
    X, y = data
    m = sc.SoftContextTabICL(**kw(ckpt))
    a = m.predict_proba(X[:60], np.eye(3)[y[:60]], X[60:])
    b = m.predict_proba(X[:60], np.full((60, 3), 1 / 3), X[60:])
    assert not np.allclose(a, b, atol=1e-4)
    assert np.allclose(b.sum(1), 1, atol=1e-5)


def test_embedding_is_convex_combination():
    from tabicl._model.layers import OneHotAndLinear
    torch.manual_seed(1)
    enc = OneHotAndLinear(4, 6)
    Q = np.array([[0.2, 0.3, 0.5, 0.0], [1, 0, 0, 0]], dtype=np.float32)
    with sc.soft_labels(Q):
        e = enc(torch.zeros(3, 2))                                   # (3, 2, 6): 3 bản sao của ngữ cảnh
    E = enc(torch.arange(4).float())                                 # embedding từng lớp, ngoài khối
    want = torch.as_tensor(Q) @ E
    assert e.shape == (3, 2, 6)
    assert torch.allclose(e[0], want, atol=1e-6) and torch.allclose(e[2], want, atol=1e-6)


def test_patch_removed_after_block_and_on_error():
    from tabicl._model.layers import OneHotAndLinear
    orig = OneHotAndLinear.forward
    with pytest.raises(RuntimeError):
        with sc.soft_labels(np.eye(2)):
            raise RuntimeError("x")
    assert OneHotAndLinear.forward is orig
    with sc.soft_labels(np.eye(2)):
        pass
    assert OneHotAndLinear.forward is orig


def test_mismatched_context_raises():
    from tabicl._model.layers import OneHotAndLinear
    enc = OneHotAndLinear(3, 4)
    with sc.soft_labels(np.eye(3)):
        with pytest.raises(sc.SoftContextError):
            enc(torch.zeros(1, 5))


def test_invalid_Q_rejected():
    with pytest.raises(ValueError):
        with sc.soft_labels(np.array([[0.5, 0.2]])):
            pass


def test_dummy_labels_cover_all_classes():
    Q = np.array([[0.9, 0.1, 0.0], [0.8, 0.2, 0.0], [0.6, 0.0, 0.4], [0.7, 0.3, 0.0]])
    y = sc.dummy_labels(Q)
    assert set(y) == {0, 1, 2}


def test_mean_field_respects_candidates(ckpt, data):
    X, y = data
    rng = np.random.default_rng(1)
    L = (rng.random((60, 3)) < 0.5).astype(float)
    L[np.arange(60), y[:60]] = 1.0                                   # PLL: nhãn đúng luôn là ứng viên
    m = sc.SoftContextTabICL(**kw(ckpt))
    Q, P = sc.mean_field(m, X[:60], L, X_test=X[60:], n_iter=2, n_folds=3, rng=0)
    assert np.all(Q[L == 0] < 1e-9)
    assert np.allclose(Q.sum(1), 1) and np.allclose(P.sum(1), 1, atol=1e-5)
