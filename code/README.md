# `code/`: thư viện và bộ chạy (bản sống của bài v3)

- **Nguồn:** `de-tai-moi/G4/code` của kho `icgibbs` tại commit `120c4d9`. Khác biệt duy nhất lúc khởi tạo: `tests/test_s2_split.py` tìm bảng chọn dataset của Study 2 ở `prior/S2/`.
- Bản đóng băng, đúng như lúc sinh kết quả của bài v2: `../prior/G4/code/`. Không sửa bản đó.

| Thành phần | Nội dung |
|---|---|
| `icgibbs/` | thư viện: `sampler.py` (Gibbs, khối, Metropolis–Hastings), `conditional.py` (bọc TFM), `baselines*.py`, `baselines_cpu.py` (PL-kNN, cây tăng cường tự huấn luyện), `g7/` (dataset, nhãn yếu, phương pháp, chỉ số, ghi kết quả) |
| `run_g7.py` | bộ chạy theo ô; chạy tiếp được; `--split dev / eval / s2 / s3` mang các khoá của bài v2 |
| `run_s2_lot.sh`, `run_g7_lot.sh` | các lượt Kaggle của bài v2 (mẫu để viết lượt của v3) |
| `tests/` | pytest |

## Kiểm thử

```bash
pip install numpy scipy scikit-learn pandas torch pytest
python -m pytest -q tests        # CPU, khoảng 10 phút
```

Lần chạy đầy đủ ngày 12/11/2026 trong kho này: 166 qua, 6 bỏ qua. Năm test bỏ qua vì thiếu kho GLWS, PRODEN và gói `sarpu` (chỉ nạp lúc chạy trên Kaggle); test thứ sáu bỏ qua vì đường dẫn cũ, đã sửa và qua khi chạy lại riêng. Lần chạy đầy đủ kế tiếp phải cho 167 qua, 5 bỏ qua.

## Chạy trên Kaggle

Mẫu ô lệnh, phiên bản gói và cách đóng gói code: `../prior/G4/README.md`. Mã truy cập TabPFN chỉ qua Kaggle Secrets (`TABPFN_TOKEN`).

## Việc cần viết cho bài v3

Xem `../v3/M2_PILOT_PLAN.md` §9: split cho tập phát triển của v3, đường học của oracle ở mọi mức, điểm xuất phát từ nhãn thật (dụng cụ đo), script lượt mới, script chấm.
