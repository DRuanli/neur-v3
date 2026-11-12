"""Sinh v3/datasets/USED_DATASETS.csv: mọi dataset đã dùng ở bài v1/v2 và vai trò của nó.

Dùng để (i) chọn tập phát triển cho v3 (mọi dataset đã "cháy" đều dùng được làm tập phát triển),
(ii) LOẠI các dataset này khỏi nghiên cứu xác nhận của v3 (Study 4).
Chạy: python -I v3/datasets/make_used_datasets.py   (từ gốc kho neur-v3)
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "code"))
from icgibbs.g7 import registry as R  # noqa: E402


def main():
    rows = []

    def add(d, role, kind, study):
        for did, v in d.items():
            name, ver = v if isinstance(v, tuple) else (v, "")
            rows.append(dict(openml_id=did, name=name, openml_version=ver or "", kind=kind, role=role, study=study,
                             subsample=R.S2_SUBSAMPLE.get(did) or R.S3_SUBSAMPLE.get(did) or "",
                             group_structure_flag=int(did in (R.S1_EXCLUDE | R.S2_S1_EXCLUDE | R.S3_S1_FLAG))))
    add(R.DEV_BINARY, "development", "binary", "v1 dev")
    add(R.DEV_MULTICLASS, "development", "multiclass", "v1 dev")
    add(R.EVAL_BINARY, "confirmatory (used)", "binary", "Study 1")
    add(R.EVAL_MULTICLASS, "confirmatory (used)", "multiclass", "Study 1")
    add(R.S2_BINARY, "confirmatory (used)", "binary", "Study 2")
    add(R.S2_MULTICLASS, "confirmatory (used)", "multiclass", "Study 2")
    add(R.S3_BINARY, "confirmatory (used); S3B pending", "binary", "Study 3")
    add(R.S3_MULTICLASS, "confirmatory (used); S3B pending", "multiclass", "Study 3")
    seen = {r["openml_id"] for r in rows}
    for did, name, ver in R.S2_RESERVE_MULTICLASS:
        if did not in seen:
            rows.append(dict(openml_id=did, name=name, openml_version=ver, kind="multiclass", role="reserve (never run)",
                             study="Study 2 reserve", subsample="", group_structure_flag=0))
    out = os.path.join(HERE, "USED_DATASETS.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["study"], r["kind"], r["openml_id"])))
    by = {}
    for r in rows:
        by[r["study"]] = by.get(r["study"], 0) + 1
    print(len(rows), "dataset;", by)


if __name__ == "__main__":
    main()
