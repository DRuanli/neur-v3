# Nhật ký thực nghiệm và phân tích của bài v3

Mỗi lượt chạy hoặc phân tích một dòng, ghi ngay khi làm. Loại: **XN** (xác nhận, đã ghi trước) hoặc **TD** (thăm dò).

| Ngày | Loại | Việc | Dữ liệu | Script (commit) | Kết quả | Ghi chú |
|---|---|---|---|---|---|---|
| 12/11/2026 | TD | H-A, H-B: trần của việc chọn chuỗi; phần khoảng cách naive → oracle | Study 2, Study 3 của v2 | `analysis/v3_headroom.py` (kho icgibbs `120c4d9`; chạy lại ở kho này cho ra đúng từng ký tự) | `results/v3_headroom.txt` | không GPU |
| 12/11/2026 | TD | R-A, R-C, R-D: phần lấy lại theo loại nhãn yếu, theo dataset, theo điểm xuất phát và AUC của oracle | bảng theo dataset của Study 1, Study 2 | `analysis/v3_regimes.py` | `results/v3_regimes.txt`, `v3_regimes*.csv` | ngưỡng 2/3, 1/3, 0,02 và các khoảng chia chọn một lần, không chỉnh sau khi xem |
| 12/11/2026 | TD | R-E: tỉ giá quy đổi từ ablation cỡ dữ liệu của Study 1 | `prior/G8/results/size_curve.csv` | `analysis/v3_regimes.py` | `results/v3_exchange_rate.csv` | công thức η_low viết cùng ngày với phép so; xem `THEORY_NOTES.md` §4 |
| 12/11/2026 | kiểm số | Hai công thức tín hiệu yếu so với mô phỏng | mô phỏng | `analysis/check_eta_low.py` | `results/check_eta_low.txt` | lệch ≤ 0,0008 |
| 13/11/2026 | — | Nhận S3B / S3BC; chấm ở kho icgibbs (`ec7c868`); chép dữ liệu và báo cáo sang `prior/S3/` | Kaggle, code `b59ef14` | `prior/S3/s3b_report.py` | `prior/S3/S3B_REPORT.md` | B3 còn 5/72 ô |
| 13/11/2026 | TD | K1–K5: kiểm luận điểm tỉ giá bằng số S3B (chưa ai thấy trước 06:09 UTC) | S3B | `analysis/v3_s3b_check.py` | `results/v3_s3b_check.txt`, `v3_s3b_pairs.csv`, `v3_s3b_datasets.csv` | không có ngưỡng ghi trước |
| 13/11/2026 | TD | η_low so với số lớp C ở PLL, q 0,3 và 0,6 trên cùng dataset | bảng Study 1–2 | `analysis/v3_eta_vs_classes.py` | `results/v3_eta_vs_classes.txt`, `.csv` | chỉ 3 lần hỏng, đều ở TabPFN v2 |
| 13/11/2026 | tra tài liệu | 9 truy vấn cho khung tỉ giá; 8 trang đã mở | — | — | `V3_IDEA_CHECK_2026-11-13.md` §3, `G2/LITERATURE.md` §5 | phần LLP đã có |
