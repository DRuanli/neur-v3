# HANDOFF: trạng thái bài v3

*Cập nhật 12/11/2026. Mỗi khi trạng thái đổi, sửa tài liệu này trước tiên. Kho: `github.com/DRuanli/neur-v3`, nhánh `main`.*

## 1. Trạng thái

- **12/11/2026:** thầy quyết định tách v3 thành bài riêng, Project riêng, kho riêng. Kho này được khởi tạo cùng ngày từ kho `icgibbs` (commit `120c4d9`).
- **Đã có:** bản chụp dự án cũ (`prior/`), code sống (`code/`), sổ tay đã cập nhật cho v3, chương trình nghiên cứu bản 2, các phép tính định hướng trên dữ liệu cũ, ghi chú lý thuyết bản nháp, bản nháp kế hoạch thí điểm.
- **Chưa có:** bất kỳ thí nghiệm nào của v3; bất kỳ kết quả xác nhận nào; lần tìm tài liệu theo giao thức cho khung mới; rà độc lập cho lý thuyết mới.
- **Đang ở cổng:** G1–G2 của sổ tay cho bài v3 (chọn bài toán đã xong về hướng; tính mới của khung "tỉ giá" chưa kiểm).

## 2. Luận điểm hiện tại, trong ba câu

Đại lượng trung tâm là **tỉ giá quy đổi** η = n_eff/n: n điểm nhãn yếu đáng bao nhiêu nhãn thật đối với một TFM đóng băng. Lý thuyết cho tỉ giá trần (ở tín hiệu yếu: 1/m cho túi ngẫu nhiên cỡ m; (E[1/|S|] − 1/C)/(1 − 1/C) cho PLL). Bài đo tỉ giá, so với trần, và chỉ ra ba vùng: đạt trần, kẹt vì thuật toán, bất khả vì thông tin.

Số liệu định hướng (thăm dò, 6 dataset, một TFM): tỉ giá đo được từ dưới 0,13 tới 0,8, tăng theo độ tách lớp, và trùng dự báo tín hiệu yếu ở dataset khó nhất của PLL (0,38 so với 0,388). Chi tiết: `v3/FINDINGS.md` §3.3, `v3/THEORY_NOTES.md` §4.

## 3. Việc kế tiếp, theo thứ tự

| # | Việc | Ai | Điều kiện |
|---|---|---|---|
| 1 | Thầy đọc `v3/V3_PLAN.md` và trả lời Q1–Q4 ở §9 | thầy | — |
| 2 | **M0b:** tìm tài liệu theo giao thức cho khung tỉ giá và hai công thức (`v3/G2/LITERATURE.md` §4); lập `REFERENCE_CHECK.md` của v3 | em | sau 1 |
| 3 | **M0b:** rà độc lập `v3/THEORY_NOTES.md` (một agent chưa tham gia) | em | sau 1 |
| 4 | Thầy chạy S3B / S3BC của bài v2 (gói `s2_code_v16.zip`, hướng dẫn ở `prior/G4/README.md`); chấm ở kho `icgibbs`; chép kết quả sang `prior/` | thầy chạy, em chấm | độc lập với 1–3 |
| 5 | **M1:** tính phần khoảng cách naive → oracle mà X lấy lại trên Study 3 | em | sau 4 |
| 6 | Chốt `v3/M2_PILOT_PLAN.md`: chọn dataset bằng script, viết code (§9 của kế hoạch), viết `m2_report.py`, test, đóng băng | em; thầy duyệt | sau 2, 3 |
| 7 | Chạy M2 trên Kaggle | thầy chạy | sau 6 |
| 8 | Bắt đầu đếm dataset cho Study 4 với nguồn rộng hơn (`v3/V3_PLAN.md` §7) | em | song song từ 12/2026 |

## 4. Việc treo của bài v2 (không thuộc kho này, ghi để khỏi quên)

- S3B / S3BC chờ chạy; sau đó đưa vào bài v2 dưới dạng phân tích bổ sung ghi sau khi Study 3 đã chấm.
- Bài v2 đang ở bản nháp 3 với style NeurIPS tạm: cần chuyển sang mẫu của tạp chí thầy chọn, xử lý mục giấy phép còn treo trong checklist, và các ý nhỏ còn lại của biên bản phản biện vòng 2.
- Thầy chưa chọn tạp chí và chưa chọn tên bài cho v2.

## 5. Bản đồ kho

| Đường dẫn | Nội dung |
|---|---|
| `v3/V3_PLAN.md` | chương trình nghiên cứu bản 2 |
| `v3/FINDINGS.md` | những gì đã biết, kèm nguồn số |
| `v3/THEORY_NOTES.md` | tỉ giá trần, bản nháp |
| `v3/G2/LITERATURE.md` | tài liệu: đã đối chiếu, đã thấy, phải tra |
| `v3/G3/CLAIM_EVIDENCE_MATRIX.md` | sáu tuyên bố và bằng chứng; danh sách khẳng định không được viết |
| `v3/M2_PILOT_PLAN.md` | bản nháp thí điểm |
| `v3/OVERLAP_WITH_V2.md` | ranh giới với bài v2 |
| `v3/EXPERIMENT_LOG.md` | nhật ký |
| `v3/AI_USAGE.md` | khai báo dùng AI của bài v3 |
| `v3/analysis/`, `v3/results/` | script và đầu ra của các phép tính định hướng |
| `v3/datasets/` | danh sách dataset đã dùng và script sinh |
| `code/` | thư viện, bộ chạy `run_g7.py`, script lượt `run_s2_lot.sh`, test |
| `prior/` | bản chụp dự án cũ; xem `prior/README.md` |
| `research-handbook/` | sổ tay; chương 11 cho v3 |

## 6. Điều cần biết về code

- `code/` giống hệt `prior/G4/code/` tại thời điểm khởi tạo. Từ đây chỉ sửa `code/`.
- Bộ chạy `run_g7.py` có các khoá của bài v2 (`--split s3` chỉ chạy đúng cấu hình Study 3 và phần bổ sung S3B). Bài v3 cần một split mới cho tập phát triển của mình; xem `v3/M2_PILOT_PLAN.md` §9.
- Bộ test: 167 qua, 5 bỏ qua, trên CPU, ở lần chạy cuối trong kho cũ (commit `b59ef14`).

## 7. Ràng buộc

Xem `CLAUDE.md`.
