"""v3_eta_vs_classes.py — THĂM DÒ (13/11/2026): ở PLL, η_low(C, q) có tách "chuỗi đơn hỏng" tốt hơn chỉ số lớp C không?

Ở Study 3, q cố định 0,6 nên η_low là hàm đơn điệu của C: không tách được hai giả thuyết. Study 1 (TabPFN v2) và
Study 2 (TabICL v2) chạy PLL ở q = 0,3 và q = 0,6 trên cùng dataset, nên η_low thay đổi khi C giữ nguyên.
Kết cục: "hỏng" = chuỗi đơn lấy lại dưới 1/3 khoảng cách naive -> oracle (cùng ngưỡng với v3_regimes.py, chọn 12/11).
Chỉ số: AUC (đảo dấu để giá trị nhỏ dự báo hỏng) của η_low và của C, trên các cặp (dataset, q) có khoảng cách >= 0,02.
Chạy: python -I v3/analysis/v3_eta_vs_classes.py   (từ gốc kho neur-v3)
"""
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v3_regimes import eta_low_pll  # noqa: E402

PRIOR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "prior")
OUT = os.path.join(os.path.dirname(HERE), "results")


def main():
    d = pd.read_csv(os.path.join(OUT, "v3_regimes_datasets.csv"))
    d = d[d.setting.str.startswith("pll")].copy()
    d["q"] = d.setting.str.split("_").str[1].astype(float)
    a = pd.read_csv(os.path.join(PRIOR, "docs", "dataset_hashes.csv"))[["name", "n_classes", "n"]].drop_duplicates("name")
    b = pd.read_csv(os.path.join(PRIOR, "S2", "census", "s2_census_candidates.csv"))[["name", "n_classes", "n"]].drop_duplicates("name")
    meta = pd.concat([a, b[~b.name.isin(a.name)]]).rename(columns={"name": "dataset", "n_classes": "C"})
    d = d.merge(meta, on="dataset", how="left")
    miss = d[d.C.isna()].dataset.unique().tolist()
    d = d.dropna(subset=["C", "recovered"])
    d["C"] = d.C.astype(int)
    d["eta_low"] = [eta_low_pll(c, q) for c, q in zip(d.C, d.q)]
    d["failed"] = (d.recovered < 1 / 3).astype(int)
    d.to_csv(os.path.join(OUT, "v3_eta_vs_classes.csv"), index=False)
    print("không tìm được số lớp:", miss)
    print(d[["study", "dataset", "C", "q", "eta_low", "recovered", "failed"]].sort_values(["study", "dataset", "q"]).round(3).to_string(index=False))
    for st, h in list(d.groupby("study")) + [("cả hai", d)]:
        if h.failed.nunique() < 2:
            print(f"\n{st}: chỉ một loại kết cục, bỏ qua")
            continue
        auc_eta = roc_auc_score(h.failed, -h.eta_low)
        auc_c = roc_auc_score(h.failed, h.C)
        auc_q = roc_auc_score(h.failed, h.q)
        print(f"\n{st}: {len(h)} cặp, {int(h.failed.sum())} hỏng.  AUC dự báo hỏng: η_low {auc_eta:.2f};  C {auc_c:.2f};  q {auc_q:.2f}")
        # cùng dataset, hai mức q: η_low giảm khi q tăng; có bao nhiêu dataset chuyển từ không hỏng sang hỏng, và ngược lại?
        w = h.pivot_table(index="dataset", columns="q", values="failed")
        if {0.3, 0.6} <= set(w.columns):
            w = w.dropna()
            print(f"   cùng dataset: q 0,3 -> 0,6: không hỏng -> hỏng {int(((w[0.3] == 0) & (w[0.6] == 1)).sum())};"
                  f" hỏng -> không hỏng {int(((w[0.3] == 1) & (w[0.6] == 0)).sum())}; giữ nguyên {int((w[0.3] == w[0.6]).sum())}")


if __name__ == "__main__":
    main()
