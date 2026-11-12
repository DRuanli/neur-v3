# Nhật ký thực nghiệm và phân tích của bài v3

Mỗi lượt chạy hoặc phân tích một dòng, ghi ngay khi làm. Loại: **XN** (xác nhận, đã ghi trước) hoặc **TD** (thăm dò).

| Ngày | Loại | Việc | Dữ liệu | Script (commit) | Kết quả | Ghi chú |
|---|---|---|---|---|---|---|
| 12/11/2026 | TD | H-A, H-B: trần của việc chọn chuỗi; phần khoảng cách naive → oracle | Study 2, Study 3 của v2 | `analysis/v3_headroom.py` (kho icgibbs `120c4d9`; chạy lại ở kho này cho ra đúng từng ký tự) | `results/v3_headroom.txt` | không GPU |
| 12/11/2026 | TD | R-A, R-C, R-D: phần lấy lại theo loại nhãn yếu, theo dataset, theo điểm xuất phát và AUC của oracle | bảng theo dataset của Study 1, Study 2 | `analysis/v3_regimes.py` | `results/v3_regimes.txt`, `v3_regimes*.csv` | ngưỡng 2/3, 1/3, 0,02 và các khoảng chia chọn một lần, không chỉnh sau khi xem |
| 12/11/2026 | TD | R-E: tỉ giá quy đổi từ ablation cỡ dữ liệu của Study 1 | `prior/G8/results/size_curve.csv` | `analysis/v3_regimes.py` | `results/v3_exchange_rate.csv` | công thức η_low viết cùng ngày với phép so; xem `THEORY_NOTES.md` §4 |
| 12/11/2026 | kiểm số | Hai công thức tín hiệu yếu so với mô phỏng | mô phỏng | `analysis/check_eta_low.py` | `results/check_eta_low.txt` | lệch ≤ 0,0008 |
