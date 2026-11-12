"""v3_regimes.py — phép tính THĂM DÒ trên dữ liệu đã có (12/11/2026), không chạy GPU, để định hướng bài v3.

Câu hỏi: ở từng loại nhãn yếu và từng mức, một chuỗi đơn lấy lại bao nhiêu phần khoảng cách
"TFM ngây thơ -> oracle có nhãn thật", và phần đó phân bố thế nào giữa các dataset?

  R-A  Study 1 (TabPFN v2, 10 dataset; LLP 3 mức, PLL 2, PU-SAR 2, nhãn nhiễu 2, bán giám sát 2; bỏ PU-SCAR vì metric
       của nó là log loss khớp tiên nghiệm, thấp hơn là tốt hơn).
  R-B  Study 2 (TabICL v2, 18 dataset, 3 mức).
Với mỗi mức: trung bình naive / chuỗi đơn / baseline tune tốt nhất / oracle; phần lấy lại = (chuỗi − naive)/(oracle − naive)
tính trên TRUNG BÌNH theo dataset; rồi theo từng dataset có khoảng cách >= GAP_MIN: số dataset "dễ" (lấy lại >= 2/3),
"dở dang" (1/3 .. 2/3), "hỏng" (< 1/3, kể cả âm).

Các ngưỡng 2/3, 1/3, GAP_MIN được đặt TRƯỚC khi chạy script này lần đầu và không chỉnh sau đó. Đây vẫn là phân tích hậu nghiệm:
không dùng làm khẳng định, chỉ để chọn lưới cho thí điểm M2.
Chạy: python -I v3/analysis/v3_regimes.py   (từ gốc kho neur-v3)
"""
import glob
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
PRIOR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "prior")
OUT = os.path.join(os.path.dirname(HERE), "results")
GAP_MIN = 0.02


def one(path, study):
    t = pd.read_csv(path, index_col=0)
    name = os.path.basename(path).replace("s2_table_", "").replace("table_", "").replace(".csv", "")
    if not {"naive", "oracle", "gibbs_warm"} <= set(t.columns) or name.startswith("pu_scar"):
        return None, None  # PU-SCAR dùng log loss khớp tiên nghiệm (thấp hơn là tốt hơn): không thuộc phép tính này
    tun = [c for c in t.columns if c.endswith("_tun")]
    best = t[tun].mean().idxmax() if tun else None
    nv, gb, orc = t.naive.mean(), t.gibbs_warm.mean(), t.oracle.mean()
    gap = t.oracle - t.naive
    frac = ((t.gibbs_warm - t.naive) / gap)[gap >= GAP_MIN]
    row = dict(study=study, setting=name, n=len(t), naive=nv, chain=gb, best_tuned=t[best].mean() if best else float("nan"),
               best_tuned_name=best, oracle=orc, gap=orc - nv,
               recovered=(gb - nv) / (orc - nv) if orc - nv > 1e-9 else float("nan"),
               recovered_best_tuned=(t[best].mean() - nv) / (orc - nv) if best and orc - nv > 1e-9 else float("nan"),
               n_gap=int((gap >= GAP_MIN).sum()), easy=int((frac >= 2 / 3).sum()),
               partial=int(((frac >= 1 / 3) & (frac < 2 / 3)).sum()), failed=int((frac < 1 / 3).sum()),
               negative=int((frac < 0).sum()), chain_above_oracle=int((t.gibbs_warm > t.oracle).sum()))
    per = pd.DataFrame(dict(study=study, setting=name, dataset=t.index, naive=t.naive.values, chain=t.gibbs_warm.values,
                            oracle=t.oracle.values, gap=gap.values,
                            recovered=((t.gibbs_warm - t.naive) / gap.where(gap >= GAP_MIN)).values))
    return row, per


def main():
    rows, pers = [], []
    for study, pat in (("S1 TabPFN v2", os.path.join(PRIOR, "G8", "results", "table_*.csv")),
                       ("S2 TabICL v2", os.path.join(PRIOR, "S2", "results", "s2_table_*.csv"))):
        for f in sorted(glob.glob(pat)):
            r, p = one(f, study)
            if r:
                rows.append(r)
                pers.append(p)
    d = pd.DataFrame(rows)
    os.makedirs(OUT, exist_ok=True)
    d.to_csv(os.path.join(OUT, "v3_regimes.csv"), index=False)
    pd.concat(pers).to_csv(os.path.join(OUT, "v3_regimes_datasets.csv"), index=False)
    pd.set_option("display.width", 250)
    show = d[["study", "setting", "n", "naive", "best_tuned", "chain", "oracle", "gap", "recovered", "recovered_best_tuned",
              "n_gap", "easy", "partial", "failed", "negative", "chain_above_oracle"]]
    print("## Phần khoảng cách naive -> oracle mà MỘT chuỗi lấy lại (thăm dò; ngưỡng dataset: khoảng cách >= %.2f)" % GAP_MIN)
    print(show.round(3).to_string(index=False))
    # R-C: phần lấy lại là tính chất của dataset hay của mức nhãn yếu? Tương quan hạng giữa các mức (Study 1).
    per = pd.concat(pers)
    print("\n## R-C. Tương quan hạng (Spearman) của phần lấy lại theo dataset giữa các mức, Study 1")
    for a, b in (("llp8", "llp_16"), ("llp8", "llp_32"), ("llp_16", "llp_32"), ("pll_0.3", "pll_0.6")):
        w = per[per.study.str.startswith("S1") & per.setting.isin([a, b])].pivot(index="dataset", columns="setting", values="recovered").dropna()
        print(f"  {a:8s} ~ {b:8s}: rho = {w[a].corr(w[b], method='spearman'):+.2f}  (n = {len(w)})")
    w = per[per.study.str.startswith("S1") & per.setting.isin(["llp8", "llp_16", "llp_32"])].pivot(index="dataset", columns="setting", values="recovered")
    print("\n## LLP, Study 1: phần lấy lại theo dataset")
    print(w[["llp8", "llp_16", "llp_32"]].round(2).to_string())
    llp_start_and_oracle()
    exchange_rate()


def eta_low_llp(m):
    """Giới hạn tín hiệu yếu (xem v3/THEORY_NOTES.md §1): một túi ngẫu nhiên cỡ m mang thông tin Fisher về hệ số của
    feature (đã quy tâm) bằng MỘT điểm có nhãn, nên tỉ giá là 1/m."""
    return 1.0 / m


def eta_low_pll(C, q):
    """Giới hạn tín hiệu yếu cho PLL nhiễu đều: (E[1/|S|] - 1/C) / (1 - 1/C), |S| = 1 + Bin(C-1, q)."""
    from math import comb
    e = sum(comb(C - 1, j) * q ** j * (1 - q) ** (C - 1 - j) / (1 + j) for j in range(C))
    return (e - 1.0 / C) / (1 - 1.0 / C)


def exchange_rate():
    """R-E: tỉ giá quy đổi nhãn yếu -> nhãn thật, từ ablation cỡ dữ liệu của Study 1 (TabPFN v2, một chuỗi; LLP túi 8 và
    PLL q 0,3; 3 dataset lớn nhất mỗi nhóm). n_eff(n) = số nhãn thật mà oracle cần để đạt đúng chỉ số của chuỗi chạy trên n
    điểm nhãn yếu, nội suy tuyến tính theo log n giữa các mốc đã chạy; tỉ giá = n_eff / n. Ngoài khoảng đã chạy thì chỉ có
    cận (ký hiệu < hoặc >). Với n > 2.000 chuỗi bị giới hạn ngữ cảnh 2.000 điểm, nên đọc cột n <= 2.000 trước."""
    import numpy as np
    C = {"optdigits": 10, "satimage": 6, "first-order-theorem-proving": 6}
    d = pd.read_csv(os.path.join(PRIOR, "G8", "results", "size_curve.csv"))
    rows = []
    for (st, ds), g in d.groupby(["setting", "dataset"]):
        g = g.sort_values("n_train")
        n, orc, ch = g.n_train.to_numpy(float), g.oracle.to_numpy(float), g.gibbs_warm.to_numpy(float)
        low = eta_low_llp(8) if st == "llp" else eta_low_pll(C[ds], 0.3)
        for ni, ci in zip(n, ch):
            if ci < orc[0]:
                ne, sign = n[0], "<"
            elif ci > orc.max():
                ne, sign = n[int(np.argmax(orc))], ">"
            else:
                j = int(np.searchsorted(orc, ci, side="right")) - 1
                j = min(max(j, 0), len(n) - 2)
                w = (ci - orc[j]) / (orc[j + 1] - orc[j]) if orc[j + 1] > orc[j] else 0.0
                ne, sign = float(np.exp(np.log(n[j]) + w * (np.log(n[j + 1]) - np.log(n[j])))), ""
            rows.append(dict(setting=st, dataset=ds, n=int(ni), chain=ci, oracle_same_n=float(orc[list(n).index(ni)]),
                             n_eff=round(ne), bound=sign, rate=round(ne / ni, 3), eta_low=round(low, 3)))
    r = pd.DataFrame(rows)
    r.to_csv(os.path.join(OUT, "v3_exchange_rate.csv"), index=False)
    print("\n## R-E. Tỉ giá quy đổi (thăm dò): n điểm nhãn yếu ~ n_eff nhãn thật; eta_low = dự báo ở giới hạn tín hiệu yếu")
    print(r.to_string(index=False))


def llp_start_and_oracle():
    """R-D (LLP, cả hai study): phần lấy lại của chuỗi so với (i) chất lượng điểm xuất phát (DLLP tuyến tính mặc định, cùng
    thước đo) và (ii) AUC của oracle. Các khoảng chia được đặt trước khi xem bảng này."""
    rows = []
    for study, pat in (("S1", os.path.join(PRIOR, "G8", "results", "table_llp*.csv")),
                       ("S2", os.path.join(PRIOR, "S2", "results", "s2_table_llp8.csv"))):
        for f in sorted(glob.glob(pat)):
            t = pd.read_csv(f, index_col=0)
            gap = t.oracle - t.naive
            best = t[[c for c in t.columns if c.endswith("_tun")]].max(axis=1)
            rows.append(pd.DataFrame(dict(study=study, setting=os.path.basename(f).replace(".csv", ""), dataset=t.index,
                                          oracle=t.oracle.values, start=((t.dllplin_def - t.naive) / gap).values,
                                          chain=((t.gibbs_warm - t.naive) / gap).values, best=((best - t.naive) / gap).values,
                                          short=(t.oracle - t.gibbs_warm).values)))
    d = pd.concat(rows)
    d.to_csv(os.path.join(OUT, "v3_regimes_llp_start.csv"), index=False)
    print("\n## R-D. LLP: chuỗi so với điểm xuất phát và so với AUC của oracle (48 cặp dataset x mức; S1 3 mức, S2 1 mức)")
    for (st, se), g in d.groupby(["study", "setting"]):
        print(f"  {st} {se:14s} n={len(g):2d}  rho(xuất phát, chuỗi) = {g.start.corr(g.chain, method='spearman'):+.2f}   "
              f"chuỗi > xuất phát: {int((g.chain > g.start).sum())}/{len(g)}   rho(AUC oracle, chuỗi) = {g.oracle.corr(g.chain, method='spearman'):+.2f}")
    d["khoang_xuat_phat"] = pd.cut(d.start, [-9, 0.2, 0.4, 0.6, 9])
    print(d.groupby("khoang_xuat_phat", observed=True).agg(n=("chain", "size"), xuat_phat=("start", "mean"), chuoi=("chain", "mean")).round(2).to_string())
    d["khoang_oracle"] = pd.cut(d.oracle, [0, 0.8, 0.9, 0.95, 1.01])
    print(d.groupby("khoang_oracle", observed=True).agg(n=("chain", "size"), auc_oracle=("oracle", "mean"), chuoi_lay_lai=("chain", "mean"),
                                                         baseline_tot_nhat_lay_lai=("best", "mean"), auc_con_thieu=("short", "mean")).round(3).to_string())


if __name__ == "__main__":
    main()
