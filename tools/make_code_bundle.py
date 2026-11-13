"""make_code_bundle.py — đóng gói thư mục code/ thành gói gửi Kaggle (v3_code_vN).

Tạo:
  _bundles/v3_code_vN/code/...            bản sao code/ (bỏ __pycache__, .pytest_cache, *.pyc)
  _bundles/v3_code_vN/MANIFEST_sha256.txt mã băm mọi file .py và .sh, cùng định dạng mà script lượt tính trên Kaggle
                                          (đường dẫn "./..." tính từ code/), để tools/intake_results.py so khớp
  _bundles/v3_code_vN/BUNDLE_INFO.txt     commit git, ngày giờ, phiên bản
  _bundles/v3_code_vN/dataset-metadata.json  (chỉ khi có --kaggle-user) để đẩy bằng Kaggle CLI
  _bundles/v3_code_vN.zip                 bản nén để tải lên Kaggle bằng giao diện web

Quy tắc: từ chối đóng gói nếu code/ còn thay đổi chưa commit (gói phải truy được về đúng một commit).
Thư mục _bundles/ nằm trong .gitignore.

Chạy (từ gốc kho):  python -I tools/make_code_bundle.py 1 [--kaggle-user TEN] [--allow-dirty]
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".ipynb_checkpoints"}


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True).stdout.strip()


def manifest(code_dir):
    rows = []
    for d, dirs, files in os.walk(code_dir):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(files):
            if f.endswith((".py", ".sh")):
                p = os.path.join(d, f)
                rel = "./" + os.path.relpath(p, code_dir).replace(os.sep, "/")
                rows.append((rel, hashlib.sha256(open(p, "rb").read()).hexdigest()))
    return sorted(rows)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("version", type=int)
    ap.add_argument("--out", default=os.path.join(ROOT, "_bundles"))
    ap.add_argument("--kaggle-user", default=None, help="tên người dùng Kaggle, để ghi dataset-metadata.json")
    ap.add_argument("--allow-dirty", action="store_true", help="chỉ để thử; gói như vậy không dùng cho lượt thật")
    a = ap.parse_args(argv)
    src = os.path.join(ROOT, "code")
    dirty = git("status", "--porcelain", "--", "code")
    if dirty and not a.allow_dirty:
        print("code/ còn thay đổi chưa commit; commit trước khi đóng gói:\n" + dirty)
        return 1
    name = f"v3_code_v{a.version}"
    dst = os.path.join(a.out, name)
    if os.path.exists(dst) or os.path.exists(dst + ".zip"):
        print(f"{dst} đã có; mỗi phiên bản chỉ đóng gói một lần (tăng số phiên bản)")
        return 1
    os.makedirs(a.out, exist_ok=True)
    shutil.copytree(src, os.path.join(dst, "code"),
                    ignore=shutil.ignore_patterns(*SKIP_DIRS, "*.pyc"))
    rows = manifest(os.path.join(dst, "code"))
    with open(os.path.join(dst, "MANIFEST_sha256.txt"), "w") as f:
        f.writelines(f"{h}  {p}\n" for p, h in rows)
    commit = git("rev-parse", "HEAD")
    with open(os.path.join(dst, "BUNDLE_INFO.txt"), "w") as f:
        f.write(f"bundle {name}\ncommit {commit}\ndirty {bool(dirty)}\ncreated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC\n"
                f"files_hashed {len(rows)}\n")
    if a.kaggle_user:
        json.dump({"title": "neur-v3-code", "id": f"{a.kaggle_user}/neur-v3-code",
                   "licenses": [{"name": "other"}]}, open(os.path.join(dst, "dataset-metadata.json"), "w"), indent=1)
    with zipfile.ZipFile(dst + ".zip", "w", zipfile.ZIP_DEFLATED) as z:
        for d, _, files in os.walk(dst):
            for f in files:
                p = os.path.join(d, f)
                z.write(p, os.path.relpath(p, a.out))
    print(f"{name}: {len(rows)} file .py/.sh, commit {commit[:7]}{' (CÓ THAY ĐỔI CHƯA COMMIT)' if dirty else ''}\n"
          f"  thư mục: {dst}\n  zip: {dst}.zip")
    return 0


if __name__ == "__main__":
    sys.exit(main())
