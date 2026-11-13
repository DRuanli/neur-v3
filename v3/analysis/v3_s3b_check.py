"""v3_s3b_check.py — kiểm lại luận điểm của v3 bằng kết quả S3B / S3BC (13/11/2026). THĂM DÒ.

Số naive, hard-EM, oracle (B2) và baseline CPU (B1) trên 20 dataset của Study 3 là số MỚI: chưa ai nhìn thấy trước
13/11/2026 06:09 UTC, khi `prior/S3/s3b_report.py` chạy. Các khuôn mẫu đem ra kiểm ở đây (R-D, công thức η_low) được viết
ngày 12/11/2026 trên Study 1–2, TRƯỚC khi có các số này. Không có dự đoán nào được ghi trước dưới dạng ngưỡng, nên đây vẫn
là phân tích thăm dò; nó chỉ cho biết khuôn mẫu cũ có lặp lại trên dữ liệu chưa thấy hay không.

  K1  Phần khoảng cách naive -> oracle mà v1 (một chuỗi), A1 (nhiều điểm xuất phát), X (nhiều TFM) lấy lại: mốc M1.
  K2  Lặp lại R-D: ở LLP, phần lấy lại tăng theo AUC của oracle? (cùng khoảng chia với R-D)
  K3  Các phương pháp có hội tụ về cùng một mức không (dấu hiệu giới hạn do thông tin), hay toả rộng (giới hạn do thuật toán)?
  K4  PLL: η_low(C, q = 0,6) và η_low·n so với độ khó đo được trên 8 dataset.
  K5  B3 (chuỗi 100 vòng, xem tạm 67/72 ô): chuỗi kẹt hay leo chậm?
Chạy: python -I v3/analysis/v3_s3b_check.py   (từ gốc kho neur-v3)
"""
import glob
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v3_regimes import eta_low_pll  # noqa: E402

PRIOR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "prior")
RES = os.path.join(PRIOR, "S3", "results")
OUT = os.path.join(os.path.dirname(HERE), "results")
Q = 0.6
BANDS = [0, 0.8, 0.9, 0.95, 1.01]


def sp(a, b):
    return pd.Series(a).corr(pd.Series(b), method="spearman")


def meta():
    rows = []
    for f in sorted(glob.glob(os.path.join(PRIOR, "S3", "raw", "S3", "s3_npz", "v1_*_s0.npz"))):
        b = os.path.basename(f)[3:-7]
        backend, rest = b.rsplit("_", 3)[0], b.rsplit("_", 3)[1:]
        did, setting = int(rest[0]), rest[1]
        z = np.load(f, allow_pickle=False)
        rows.append(dict(dataset_id=did, setting=setting, n_train=len(z["ytr"]), C=z["Q_warm"].shape[1]))
    return pd.DataFrame(rows).drop_duplicates(["dataset_id", "setting"])


def main():
    pairs = pd.read_csv(os.path.join(RES, "s3b_tfm_pairs.csv"))
    ds = pd.read_csv(os.path.join(RES, "s3_datasets.csv"))
    cpu = pd.read_csv(os.path.join(RES, "s3b_cpu_datasets.csv"))
    m = meta()
    g = pairs.m_oracle - pairs.m_naive
    for c, col in (("v1", "v1"), ("A1", "A1"), ("hardem", "m_hard_em_warm"), ("L", "L")):
        pairs[f"rec_{c}"] = (pairs[col] - pairs.m_naive) / g
    pairs.to_csv(os.path.join(OUT, "v3_s3b_pairs.csv"), index=False)

    d = pairs.groupby(["setting", "dataset_id"]).agg(naive=("m_naive", "mean"), oracle=("m_oracle", "mean"),
                                                     best_oracle=("m_oracle", "max"), v1=("v1", "mean"), A1=("A1", "mean"),
                                                     hardem=("m_hard_em_warm", "mean"), n_tfm=("v1", "size")).reset_index()
    d = d.merge(ds[["dataset_id", "X", "meanL"]], on="dataset_id").merge(
        cpu[["dataset_id", "gbdtself_def", "plknn_def", "best_cpu"]], on="dataset_id").merge(m, on=["dataset_id", "setting"])
    gap = d.oracle - d.naive
    for c in ("v1", "A1", "X", "hardem", "meanL", "best_cpu"):
        d[f"rec_{c}"] = (d[c] - d.naive) / gap
    d["rec_X_vs_best_oracle"] = (d.X - d.naive) / (d.best_oracle - d.naive)
    meth = ["v1", "hardem", "meanL", "best_cpu"]
    d["spread"] = d[meth].max(axis=1) - d[meth].min(axis=1)
    d["rel_spread"] = d.spread / gap
    d["eta_low"] = np.where(d.setting == "llp", 1 / 8, [eta_low_pll(int(c), Q) for c in d.C])
    d["eta_low_n"] = d.eta_low * d.n_train
    d.to_csv(os.path.join(OUT, "v3_s3b_datasets.csv"), index=False)
    pd.set_option("display.width", 250)

    print("## K1. Phần khoảng cách naive -> oracle được lấy lại (oracle = trung bình trên các TFM đã chạy dataset đó)")
    for st, h in d.groupby("setting"):
        gp = (h.oracle - h.naive).mean()
        line = [f"{st}: n = {len(h)}; naive {h.naive.mean():.3f}, oracle {h.oracle.mean():.3f}"]
        for c in ("v1", "hardem", "meanL", "best_cpu", "A1", "X"):
            line.append(f"{c} {(h[c].mean() - h.naive.mean()) / gp:.2f} (trung vị theo dataset {h['rec_' + c].median():.2f})")
        print("  " + "; ".join(line))
        print(f"     X so với oracle tốt nhất: {((h.X - h.naive).mean() / (h.best_oracle - h.naive).mean()):.2f}")
    pr = pairs.groupby("setting")
    print("  theo cặp (TFM, dataset), cùng một TFM: " + "; ".join(
        f"{st}: v1 {((h.v1 - h.m_naive).mean() / (h.m_oracle - h.m_naive).mean()):.2f}, A1 {((h.A1 - h.m_naive).mean() / (h.m_oracle - h.m_naive).mean()):.2f}"
        f", hard-EM {((h.m_hard_em_warm - h.m_naive).mean() / (h.m_oracle - h.m_naive).mean()):.2f} (n = {len(h)})" for st, h in pr))

    print("\n## K2. Lặp lại R-D (LLP): phần lấy lại của một chuỗi theo AUC của oracle; R-D trên Study 1–2 cho 0,25 / 0,53 / 0,70 / 0,79")
    h = pairs[pairs.setting == "llp"].copy()
    h["band"] = pd.cut(h.m_oracle, BANDS)
    print(h.groupby("band", observed=True).agg(n=("rec_v1", "size"), oracle=("m_oracle", "mean"), rec_v1=("rec_v1", "mean"),
                                                rec_hardem=("rec_hardem", "mean"), rec_A1=("rec_A1", "mean")).round(2).to_string())
    print(f"  rho(AUC oracle, phần lấy lại của v1) = {sp(h.m_oracle, h.rec_v1):+.2f} trên {len(h)} cặp; "
          f"theo dataset (trung bình TFM): {sp(d[d.setting == 'llp'].oracle, d[d.setting == 'llp'].rec_v1):+.2f} trên 12")

    print("\n## K3. Các phương pháp hội tụ hay toả rộng? spread = max − min của {v1, hard-EM, L, baseline CPU tốt nhất}")
    for st, h in d.groupby("setting"):
        print(f"  {st}: trung vị spread {h.spread.median():.3f}, trung vị spread / khoảng cách {h.rel_spread.median():.2f}; "
              f"số dataset có spread < 0,03: {int((h.spread < 0.03).sum())}/{len(h)}")
    print("  LLP, chênh trung bình theo dataset: v1 − hard-EM {:+.3f}; v1 − GBDT tự huấn luyện {:+.3f}; L − GBDT {:+.3f}".format(
        *[(d[d.setting == "llp"][a] - d[d.setting == "llp"][b]).mean() for a, b in (("v1", "hardem"), ("v1", "gbdtself_def"), ("meanL", "gbdtself_def"))]))

    print("\n## K4. PLL: η_low ở q = 0,6 và độ khó (8 dataset)")
    h = d[d.setting == "pll"].sort_values("eta_low")
    print(h[["dataset_id", "C", "n_train", "eta_low", "eta_low_n", "naive", "oracle", "v1", "A1", "X", "rec_v1", "rec_X", "spread"]].round(3).to_string(index=False))
    for c in ("rec_v1", "rec_A1", "rec_X", "spread"):
        print(f"  rho(η_low, {c}) = {sp(h.eta_low, h[c]):+.2f};  rho(η_low·n, {c}) = {sp(h.eta_low_n, h[c]):+.2f}")

    print("\n## K5. B3 xem tạm (67/72 ô; thiếu 3 seed TabICL v2 và 2 seed TabPFN-3 của dataset 46933): độ đúng nhãn của chuỗi ấm ở vòng 30 và vòng 100")
    j = pd.read_csv(os.path.join(RES, "s3b_long_cells.csv"))
    for t, h in j.groupby("backend"):
        s = h[h.T2 == 1]
        print(f"  {t:10s} {len(h)} ô; kẹt {len(s)}, sửa được {int(s.repaired.sum())}; lợi trung bình {h.gain.mean():+.3f}"
              f" (ô kẹt {s.gain.mean():+.3f}); r30 {h.r30.mean():.3f} -> r100 {h.r100.mean():.3f}; còn đang tăng {int(h.still_rising.sum())}")
    s = j[j.T2 == 1]
    print(f"  cả {len(j)} ô: kẹt {len(s)}, sửa được {int(s.repaired.sum())} ({s.repaired.mean():.0%}); lợi trung bình {j.gain.mean():+.3f}")
    left = 72 - len(j)
    print(f"  {left} ô còn thiếu: dù mỗi ô có lợi 0, lợi trung bình trên 72 ô vẫn là {j.gain.sum() / 72:+.3f} (ngưỡng P22: 0,03)")


if __name__ == "__main__":
    main()
