"""intake_results.py — nhận kết quả một lượt Kaggle một cách an toàn và kiểm trước khi dùng.

Kết quả tải về là dữ liệu KHÔNG tin cậy. Script này:
  1. giải nén từng zip vào một thư mục MỚI, TRỐNG: _incoming/<LOT>_<thời điểm>/ (từ chối đường dẫn tuyệt đối, "..",
     liên kết tượng trưng); không chạy bất kỳ code nào trong đó;
  2. so mã băm code đã chạy (*_code_sha256.txt do script lượt ghi) với MANIFEST_sha256.txt của gói đã gửi;
  3. đọc dòng cuối của log pytest; đếm dòng và trạng thái của mọi CSV kết quả; liệt kê npz, log;
  4. ghi INTAKE_REPORT.json và in tóm tắt. Không chép gì vào kho: việc chép do người hoặc agent làm sau khi đọc báo cáo.

Chạy (từ gốc kho):
  python -I tools/intake_results.py --lot A1 --bundle _bundles/v3_code_v1 KET_QUA_1.zip [KET_QUA_2.zip ...]
Mã thoát: 0 nếu mọi kiểm tra qua; 2 nếu có điểm không khớp (vẫn ghi báo cáo).
"""
import argparse
import csv
import datetime as dt
import glob
import json
import os
import stat
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def safe_extract(zpath, dst):
    bad = []
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            name = info.filename
            mode = info.external_attr >> 16
            if os.path.isabs(name) or ".." in name.replace("\\", "/").split("/") or stat.S_ISLNK(mode):
                bad.append(name)
                continue
            z.extract(info, dst)
    return bad


def read_manifest(path):
    out = {}
    for line in open(path):
        if line.strip():
            h, p = line.split(None, 1)
            out[p.strip()] = h
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("zips", nargs="+")
    ap.add_argument("--lot", required=True)
    ap.add_argument("--bundle", required=True, help="thư mục gói đã gửi, có MANIFEST_sha256.txt")
    ap.add_argument("--out", default=os.path.join(ROOT, "_incoming"))
    a = ap.parse_args(argv)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(a.out, f"{a.lot}_{stamp}")
    os.makedirs(dst, exist_ok=False)
    rep = {"lot": a.lot, "dir": dst, "zips": a.zips, "problems": []}
    for z in a.zips:
        sub = os.path.join(dst, os.path.splitext(os.path.basename(z))[0])
        os.makedirs(sub)
        bad = safe_extract(z, sub)
        if bad:
            rep["problems"].append(f"{z}: bỏ qua {len(bad)} mục nguy hiểm (đường dẫn tuyệt đối, '..', symlink)")
    ref = read_manifest(os.path.join(a.bundle, "MANIFEST_sha256.txt"))
    rep["bundle"] = open(os.path.join(a.bundle, "BUNDLE_INFO.txt")).read().strip().splitlines()
    shas = glob.glob(os.path.join(dst, "**", "*_code_sha256.txt"), recursive=True)
    rep["code_hash"] = []
    for s in shas:
        got = read_manifest(s)
        diff = sorted(p for p in set(ref) | set(got) if ref.get(p) != got.get(p))
        rep["code_hash"].append({"file": os.path.relpath(s, dst), "n": len(got), "mismatch": diff[:20], "n_mismatch": len(diff)})
        if diff:
            rep["problems"].append(f"{os.path.basename(s)}: {len(diff)} file lệch mã băm so với gói")
    if not shas:
        rep["problems"].append("không thấy file *_code_sha256.txt: không xác minh được code đã chạy")
    rep["pytest"] = {}
    for p in glob.glob(os.path.join(dst, "**", "*_pytest.log"), recursive=True):
        lines = [x for x in open(p, errors="replace").read().splitlines() if x.strip()]
        last = lines[-1] if lines else ""
        rep["pytest"][os.path.relpath(p, dst)] = last
        if "failed" in last or "error" in last.lower():
            rep["problems"].append(f"{os.path.basename(p)}: {last}")
    rep["csv"] = {}
    for p in sorted(glob.glob(os.path.join(dst, "**", "*.csv"), recursive=True)):
        if f"{os.sep}code{os.sep}" in p:          # bản sao code đi kèm output, không phải kết quả
            continue
        with open(p, newline="", errors="replace") as f:
            rows = list(csv.DictReader(f))
        st = {}
        for r in rows:
            st[r.get("status", "?")] = st.get(r.get("status", "?"), 0) + 1
        rep["csv"][os.path.relpath(p, dst)] = {"rows": len(rows), "status": st}
    rep["n_npz"] = len(glob.glob(os.path.join(dst, "**", "*.npz"), recursive=True))
    rep["logs_with_traceback"] = [os.path.relpath(p, dst) for p in glob.glob(os.path.join(dst, "**", "*.log"), recursive=True)
                                  if "Traceback" in open(p, errors="replace").read()]
    rep["ok"] = not rep["problems"]
    json.dump(rep, open(os.path.join(dst, "INTAKE_REPORT.json"), "w"), ensure_ascii=False, indent=1)
    print(f"Lượt {a.lot}: giải nén vào {dst}")
    print(f"  mã băm code: " + "; ".join(f"{c['file']} ({c['n']} file, lệch {c['n_mismatch']})" for c in rep["code_hash"]))
    for k, v in rep["pytest"].items():
        print(f"  pytest {k}: {v}")
    for k, v in rep["csv"].items():
        print(f"  {k}: {v['rows']} dòng, trạng thái {v['status']}")
    print(f"  npz: {rep['n_npz']}; log có Traceback: {len(rep['logs_with_traceback'])}")
    print("KẾT LUẬN: " + ("mọi kiểm tra qua" if rep["ok"] else "CÓ VẤN ĐỀ:\n  - " + "\n  - ".join(rep["problems"])))
    return 0 if rep["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
