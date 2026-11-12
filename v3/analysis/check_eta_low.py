"""check_eta_low.py — kiểm số hai công thức tỉ giá ở giới hạn tín hiệu yếu (v3/THEORY_NOTES.md §1), bằng mô phỏng.

Cách kiểm: ước lượng hợp lý cực đại (một bước Newton quanh beta = 0 là đủ ở tín hiệu yếu) cần phương sai của điểm số
(score). Ta mô phỏng trực tiếp ma trận thông tin Fisher = hiệp phương sai của score tại beta = 0, cho dữ liệu đủ nhãn và
dữ liệu nhãn yếu, rồi so tỉ số vết (trace) với công thức.
  LLP: logistic, túi ngẫu nhiên cỡ m, quan sát số đếm. Score của túi theo beta (bỏ hệ số chặn): (c - m*pi) * xbar_B.
  PLL: logit đa thức C lớp, tiên nghiệm đều, mỗi nhãn sai vào tập ứng viên độc lập với xác suất q.
       Score theo hệ số của lớp k: x * (1[k in S]/|S| - 1/C).
Chạy: python -I v3/analysis/check_eta_low.py   (từ gốc kho neur-v3)
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # cần vì script chạy với python -I
from v3_regimes import eta_low_llp, eta_low_pll


def llp(m, pi=0.4, d=3, n_bags=200000, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n_bags, m, d))                 # feature đã quy tâm, hiệp phương sai đơn vị
    y = rng.random((n_bags, m)) < pi                        # beta = 0: nhãn độc lập với feature
    full = ((y - pi)[:, :, None] * X).reshape(-1, d)        # score từng điểm
    weak = (y.sum(1) - m * pi)[:, None] * X.mean(1)         # score của túi
    return np.trace(weak.T @ weak / n_bags) / np.trace(full.T @ full / n_bags), eta_low_llp(m)


def pll(C, q, n=400000, seed=0):
    rng = np.random.default_rng(seed)
    y = rng.integers(0, C, n)
    S = rng.random((n, C)) < q
    S[np.arange(n), y] = True
    full = (np.arange(C)[None, :] == y[:, None]) - 1.0 / C
    weak = S / S.sum(1, keepdims=True) - 1.0 / C
    return np.trace(weak.T @ weak / n) / np.trace(full.T @ full / n), eta_low_pll(C, q)


if __name__ == "__main__":
    print("LLP  m   mô phỏng  công thức")
    for m in (2, 8, 32):
        a, b = llp(m, n_bags=200000 if m < 32 else 60000)
        print(f"    {m:3d}  {a:.4f}    {b:.4f}")
    print("PLL  C    q    mô phỏng  công thức")
    for C, q in ((3, 0.3), (6, 0.3), (10, 0.3), (10, 0.6), (20, 0.6), (10, 0.9)):
        a, b = pll(C, q)
        print(f"    {C:3d}  {q:.1f}  {a:.4f}    {b:.4f}")
