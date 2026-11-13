# HANDOFF: trạng thái bài v3

*Cập nhật 13/11/2026 (mục 0); phần còn lại ngày 12/11/2026. Mỗi khi trạng thái đổi, sửa tài liệu này trước tiên. Kho: `github.com/DRuanli/neur-v3`, nhánh `main`.*

## 000. Mới nhất (13/11/2026, 14 giờ): đã chốt bản 3; chuyển sang Claude Science

- **Thầy chốt kế hoạch bản 3** (13/11/2026 13:39): Q1–Q3 duyệt theo đề xuất; Q4 (đóng băng A1) duyệt khi code A1 xong.
- **Từ nay làm việc trong Claude Science** trên máy thầy, Project `neur-v3`. Hướng dẫn đầy đủ ở `docs/claude-science/`:
  - `01_CAI_DAT_MAY_LOCAL.md`: cài đặt, clone kho, khoá Kaggle;
  - `02_TAO_PROJECT.md`: tạo Project, cấp thư mục, skill, reviewer;
  - `03_QUY_TRINH_KAGGLE.md`: hai ô notebook, chế độ CLI tuỳ chọn, nhận kết quả;
  - `PROJECT_INSTRUCTIONS.md`, `REVIEWER_CRITERIA.md`, `PROMPT_KHOI_DAU.md`, `PROMPTS_NGHIEN_CUU.md` (P0–P11).
- **Công cụ mới:**
  - `tools/make_code_bundle.py`;
  - `tools/intake_results.py` (đã thử trên gói S3B thật: 87 file khớp mã băm);
  - `code/run_v3_lot.sh` với lượt SMOKE;
  - `code/smoke_softctx.py`;
  - `kaggle/templates/`.
- **Skill:** `skills/neur-v3-research`, `skills/kaggle-lot` (tải lên Claude Science dạng zip; kho quá 100 MB nên không nhập từ GitHub được).
- **Test:** 176 qua, 5 bỏ qua (CPU).
- **Việc kế tiếp, theo thứ tự:**
  1. thầy cài đặt theo `01` và `02`;
  2. phiên đầu với `PROMPT_KHOI_DAU.md`;
  3. thầy chạy lượt SMOKE trên Kaggle (vài phút, một T4, Internet On, không cần Secret);
  4. P2 nhận SMOKE;
  5. P3 hoàn tất A0 và đóng băng A1, song song P4 tra tài liệu;
  6. P1 chạy A1;
  7. P5 chuẩn bị SCI-FT.
- **Việc treo của bài v2:** phiên 2 của lượt S3B (5 ô B3) — prompt P11.

## 00. Ngày 13/11/2026 (chiều): thầy chọn hướng phát triển thuật toán

- `v3/V3_PLAN.md` nay là **bản 3**: thuật toán SCI (ngữ cảnh nhãn mềm), gồm SCI-0 (TFM đóng băng) và SCI-FT (fine-tune TabICL v2 trên bài toán nhãn yếu tổng hợp để một lượt truyền xuôi trả về dự đoán hậu nghiệm). Bản 2 ở `v3/archive/`.
- **Đã làm:** `code/icgibbs/softctx.py` (bản vá encoder nhãn của TabICL, trường trung bình trong ngữ cảnh) và `code/tests/test_softctx.py` (8 test qua trên CPU với mô hình khởi tạo ngẫu nhiên; nhãn mềm one-hot trùng nhãn cứng, lệch dưới 1e-5).
- **Bản nháp thí điểm:** `v3/A1_PILOT_PLAN.md` (SCI-0, một phiên Kaggle). Chưa đóng băng.
- **Chờ thầy:** Q1–Q4 ở `v3/V3_PLAN.md` §8.
- **Việc kế tiếp của em sau khi thầy duyệt:** gắn `sci_once`, `sci_mf` vào bộ chạy, viết lượt A1 và `a1_report.py`, test, đóng băng; song song tra tài liệu theo giao thức cho SCI-FT và viết bộ sinh bài toán nhãn yếu tổng hợp từ `tabicl.prior`.
- Môi trường này cài được `tabicl` từ PyPI nhưng **không tải được trọng số** (HuggingFace bị chặn); mọi lần chạy với trọng số thật phải làm trên Kaggle.

## 0. Ngày 13/11/2026 (sáng)

- **S3B / S3BC đã chạy và chấm** (kho `icgibbs`, commit `ec7c868`; bản sao ở `prior/S3/S3B_REPORT.md`). B1 và B2 chính thức; B3 còn thiếu 5/72 ô, chấm tạm trên TabDPT.
- **Kiểm định luận điểm v3** (`v3/V3_IDEA_CHECK_2026-11-13.md`): luận điểm "tỉ giá quy đổi" bị suy yếu nặng. Phần lý thuyết LLP đã có trong tài liệu, dự báo tín hiệu yếu sai ở dữ liệu thật, khuôn mẫu R-D không lặp lại, ranh giới vùng khó do TFM quyết định. Mốc M1 qua.
- **Đang chờ thầy:** chọn hướng A (thu hẹp thành bài đo), B (hành vi của TFM khi ngữ cảnh có nhãn sai), C (đánh giá lại học nhãn yếu trên dữ liệu bảng) hay D (dồn cho bài v2 ở tạp chí, chọn đề tài NeurIPS khác). Em đề xuất làm xong bài v2 trước; nếu vẫn nhắm NeurIPS từ dòng này thì kiểm "giết hay giữ" hướng C trong 1–2 tuần.
- **Không chạy M2** theo thiết kế hiện tại.
- **Việc của thầy:** chạy phiên 2 của lượt S3B để xong 5 ô B3 (hướng dẫn ở `prior/G4/README.md`, mục S3B: notebook mới, thêm output phiên 1, dán y hệt hai ô).

## 1. Trạng thái (12/11/2026)

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
| 6 | ~~Chốt M2~~ (huỷ 13/11: luận điểm tỉ giá đã bỏ; xem mục 00) | — | — |
| 7 | Chạy M2 trên Kaggle | thầy chạy | sau 6 |
| 8 | Bắt đầu đếm dataset cho Study 4 với nguồn rộng hơn (`v3/V3_PLAN.md` §7) | em | song song từ 12/2026 |

## 4. Việc treo của bài v2 (không thuộc kho này, ghi để khỏi quên)

- S3B / S3BC chờ chạy; sau đó đưa vào bài v2 dưới dạng phân tích bổ sung ghi sau khi Study 3 đã chấm.
- Bài v2 đang ở bản nháp 3 với style NeurIPS tạm: cần chuyển sang mẫu của tạp chí thầy chọn, xử lý mục giấy phép còn treo trong checklist, và các ý nhỏ còn lại của biên bản phản biện vòng 2.
- Thầy chưa chọn tạp chí và chưa chọn tên bài cho v2.

## 5. Bản đồ kho

| Đường dẫn | Nội dung |
|---|---|
| `v3/V3_PLAN.md` | chương trình nghiên cứu bản 3: hướng thuật toán (SCI) |
| `v3/A1_PILOT_PLAN.md` | bản nháp thí điểm SCI-0 |
| `v3/archive/` | bản 2 (tỉ giá) và bản nháp M2 cũ |
| `code/icgibbs/softctx.py` | lõi nhãn mềm cho TabICL v2 |
| `docs/claude-science/` | cài đặt Claude Science, tạo Project, quy trình Kaggle, prompt |
| `skills/` | hai skill của đề tài |
| `tools/` | đóng gói code; nhận kết quả Kaggle |
| `kaggle/templates/` | mẫu cho chế độ Kaggle CLI |
| `v3/V3_IDEA_CHECK_2026-11-13.md` | kiểm định luận điểm bằng S3B và tài liệu; ba hướng thay thế |
| `v3/FINDINGS.md` | những gì đã biết, kèm nguồn số |
| `v3/THEORY_NOTES.md` | tỉ giá trần, bản nháp |
| `v3/G2/LITERATURE.md` | tài liệu: đã đối chiếu, đã thấy, phải tra |
| `v3/G3/CLAIM_EVIDENCE_MATRIX.md` | sáu tuyên bố và bằng chứng; danh sách khẳng định không được viết |
| `v3/OVERLAP_WITH_V2.md` | ranh giới với bài v2 |
| `v3/EXPERIMENT_LOG.md` | nhật ký |
| `v3/AI_USAGE.md` | khai báo dùng AI của bài v3 |
| `v3/analysis/`, `v3/results/` | script và đầu ra của các phép tính định hướng |
| `v3/datasets/` | danh sách dataset đã dùng và script sinh |
| `code/` | thư viện, bộ chạy `run_g7.py`, script lượt `run_s2_lot.sh`, test |
| `prior/` | bản chụp dự án cũ; xem `prior/README.md` |
| `research-handbook/` | sổ tay; chương 11 cho v3 |

## 6. Điều cần biết về code

- `code/` lấy từ `prior/G4/code/`; khác biệt duy nhất lúc khởi tạo là đường dẫn trong `tests/test_s2_split.py`. Từ đây chỉ sửa `code/`.
- Bộ chạy `run_g7.py` có các khoá của bài v2 (`--split s3` chỉ chạy đúng cấu hình Study 3 và phần bổ sung S3B). Bài v3 cần gắn phương pháp mới vào bộ chạy; xem `v3/A1_PILOT_PLAN.md` §7.
- Bộ test chạy trong kho này ngày 12/11/2026: 167 qua, 5 bỏ qua (CPU, khoảng 10 phút). Lần chạy đầy đủ cho 166 qua và 6 bỏ qua vì một test tìm bảng của Study 2 theo đường dẫn của kho cũ; đã sửa đường dẫn và test đó qua khi chạy lại riêng.

## 7. Ràng buộc

Xem `CLAUDE.md`.
