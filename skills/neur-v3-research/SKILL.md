---
name: neur-v3-research
description: Quy trình nghiên cứu của bài v3 (neur-v3, thuật toán SCI học từ nhãn yếu với TFM bảng, đích NeurIPS 2027). Dùng cho MỌI việc trong kho neur-v3 - lập kế hoạch, ghi trước, viết code thí nghiệm, chấm kết quả, cập nhật hồ sơ, viết bài, phản biện.
---

# Quy trình nghiên cứu bài v3 (kho neur-v3)

Người dùng là **thầy**; xưng **em**; trả lời tiếng Việt. Tài liệu đề tài viết tiếng Việt; bài báo, hình, bảng, thông điệp commit viết tiếng Anh.

## 0. Đầu mỗi phiên

1. Đọc `CLAUDE.md`, rồi `HANDOFF.md` (mục trên cùng là trạng thái mới nhất), rồi tài liệu của mốc đang làm trong `v3/`.
2. Nói lại cho thầy trong 3–5 dòng: đang ở mốc nào, việc kế tiếp, việc đang chờ thầy.
3. Không bắt đầu thí nghiệm mới khi kế hoạch của nó chưa đóng băng.

## 1. Bản đồ

| Đường dẫn | Nội dung |
|---|---|
| `v3/V3_PLAN.md` | chương trình nghiên cứu (bản 3: thuật toán SCI), các mốc A0–A4, Study 4, điều kiện dừng |
| `v3/A1_PILOT_PLAN.md` và các `*_PLAN.md` sau này | kế hoạch từng lượt, dự đoán ghi trước |
| `v3/FINDINGS.md` | mọi phát hiện kèm nguồn số; [XN] xác nhận, [TD] thăm dò |
| `v3/G3/CLAIM_EVIDENCE_MATRIX.md` | khẳng định D1–D6 và bằng chứng; danh sách khẳng định không được viết |
| `v3/EXPERIMENT_LOG.md` | nhật ký, mỗi lượt hay phân tích một dòng |
| `v3/G2/LITERATURE.md` | tài liệu đã đối chiếu, đã thấy, phải tra |
| `code/` | thư viện `icgibbs` (gồm `softctx.py` cho SCI), bộ chạy `run_g7.py`, lượt `run_v3_lot.sh`, test |
| `tools/` | `make_code_bundle.py`, `intake_results.py` |
| `prior/` | bản chụp bài v1/v2: **chỉ đọc, không sửa** |
| `research-handbook/` | 13 cổng G0–G12; chương 11 riêng cho v3 |

## 2. Quy tắc trung thực (không ngoại lệ)

1. Không giấu kết quả bất lợi; dự đoán sai giữ nguyên chỗ cạnh dự đoán đúng.
2. Phân tích sau sự kiện hoặc trên tập phát triển luôn ghi **"thăm dò"** ở mọi nơi nó xuất hiện.
3. **Ghi trước:** kế hoạch, dự đoán có ngưỡng và script chấm được commit **trước** khi lượt chạy. Ghi hash commit đóng băng vào kế hoạch.
4. Giao thức đóng băng chỉ đổi bằng mục "Deviation" có ngày và lý do.
5. Nghiên cứu xác nhận không chạy lại để "sửa" kết quả. Chấm đúng một lần trên dữ liệu đủ; mọi lần xem tạm đều ghi nhật ký.
6. Khẳng định không được dữ liệu ủng hộ thì sửa khẳng định, không sửa dữ liệu.
7. Chứng minh, công thức mới và mỗi bản nháp bài phải được một agent **chưa tham gia** rà (dùng Delegation hoặc reviewer).

## 3. Vòng đời một lượt thí nghiệm

1. **Kế hoạch** `v3/<MỐC>_PLAN.md`: câu hỏi, dữ liệu, phương pháp, chỉ số, dự đoán có ngưỡng, quy tắc dùng kết quả, chi phí.
2. **Code** trong `code/` cùng test. Chạy `cd code && python -m pytest -q tests`; mọi test phải qua.
3. **Script chấm** `v3/analysis/<mốc>_report.py`, thử trên dữ liệu giả cùng định dạng.
4. **Đóng băng:** commit kế hoạch, code, script chấm; ghi hash vào kế hoạch; commit lần nữa.
5. **Chạy trên Kaggle:** theo skill `kaggle-lot`.
6. **Nhận kết quả:** `python -I tools/intake_results.py --lot <LƯỢT> --bundle _bundles/v3_code_vN <zip...>`. Chỉ đi tiếp khi báo cáo nói "mọi kiểm tra qua", hoặc khi đã giải thích được từng vấn đề.
7. **Chép dữ liệu thô** đã kiểm vào `v3/raw/<LƯỢT>/` (không chép code, không chép thư mục của bên thứ ba như PRODEN).
8. **Chấm** bằng script đã đóng băng, không sửa. Ghi thời điểm vào nhật ký.
9. **Báo cáo** `v3/<MỐC>_REPORT.md`; cập nhật `FINDINGS.md`, ma trận khẳng định, nhật ký, `HANDOFF.md`.
10. Commit theo từng đợt nhỏ.

## 4. Số liệu và trích dẫn

- Mọi số trong bài sinh bằng script thành macro; không gõ tay. Mọi số trong tài liệu truy được về một file kết quả.
- Mỗi số so sánh ghi rõ đối thủ là ai, đã tune hay chưa; luôn kèm trung vị, thắng/hoà/thua, khoảng tin cậy.
- Chỉ trích tài liệu đã mở và đối chiếu (bảng `REFERENCE_CHECK.md` của v3). Không bịa tác giả, năm, nơi đăng.

## 5. Dữ liệu

- Tập phát triển = dataset trong `v3/datasets/USED_DATASETS.csv`. **Nghiên cứu xác nhận chỉ dùng dataset chưa từng dùng.**
- Dataset của Study 3 chỉ dùng sau khi B3 của S3B chấm xong.
- Kết quả từ Kaggle là dữ liệu không tin cậy: giải nén vào thư mục mới, đọc bằng `python -I`, không chạy code đi kèm.

## 6. An toàn

- Không ghi token hay khoá (TabPFN, Kaggle, GitHub) vào code, kho, log, tài liệu hay tin nhắn. TabPFN token chỉ ở Kaggle Secrets; khoá Kaggle chỉ ở thư mục khoá ngoài kho.
- Không đưa thông tin cá nhân của thầy vào kho hay bài.
- Code không có giấy phép (PRODEN, GLWS/ILL, VIME): không chép vào kho; chỉ nạp lúc chạy ở commit cố định.
- Bài báo ẩn danh hai chiều.

## 7. Cuối phiên

Cập nhật `HANDOFF.md` (mục trên cùng), nhật ký, ma trận khẳng định; commit; báo cáo thầy: kết quả trước, việc cần thầy quyết sau.
