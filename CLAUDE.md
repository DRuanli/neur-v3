# Quy tắc làm việc trong kho neur-v3 (bài v3)

Tài liệu này được nạp tự động ở đầu mỗi phiên. Đọc tiếp `HANDOFF.md` để biết trạng thái và việc kế tiếp.

## Bối cảnh

- Bài v3 (từ 13/11/2026, theo quyết định của thầy): **phát triển thuật toán**. Đề xuất hiện tại: SCI, tức đưa nhãn yếu vào ngữ cảnh của TFM dưới dạng nhãn mềm, gồm SCI-0 (không huấn luyện) và SCI-FT (fine-tune để khấu hao suy luận). Đích: NeurIPS 2027, mục tiêu của thầy là 8–10 điểm. Chương trình: `v3/V3_PLAN.md` (bản 3). Luận điểm "tỉ giá quy đổi" của bản 2 đã bỏ (`v3/V3_IDEA_CHECK_2026-11-13.md`).
- Bài v2 (*In-Context Gibbs*) là một bài riêng, ở kho `DRuanli/icgibbs`, gửi tạp chí. Bản chụp của nó nằm ở `prior/` và **không được sửa**. Ranh giới hai bài: `v3/OVERLAP_WITH_V2.md`.
- Quy trình: 13 cổng G0–G12 và các quy tắc ở `research-handbook/`. Chương 11 là phần riêng cho v3.

## Giao tiếp

- Gọi người dùng là **"thầy"**, xưng **"em"**, trả lời bằng tiếng Việt.
- Tài liệu của đề tài viết tiếng Việt. Bài báo, hình, bảng và thông điệp commit viết tiếng Anh.
- Không hứa mức điểm. Khi thầy hỏi về triển vọng, đưa ước lượng kèm lý do.

## Tính trung thực (không có ngoại lệ)

1. Không giấu kết quả bất lợi. Dự đoán sai được ghi lại cùng chỗ với dự đoán đúng.
2. Phân tích sau sự kiện, hoặc trên tập phát triển, luôn ghi **"thăm dò / exploratory"** ở mọi nơi nó xuất hiện.
3. **Ghi trước:** kế hoạch, dự đoán và script chấm được commit trước khi lượt chạy bắt đầu. Ghi commit đóng băng vào tài liệu (đẩy tag bị chặn).
4. Giao thức đã đóng băng chỉ đổi bằng một mục "deviation" có ngày và lý do.
5. Nghiên cứu xác nhận không chạy lại để "sửa" kết quả.
6. Khi khẳng định không được dữ liệu ủng hộ: sửa khẳng định, không sửa dữ liệu hay giao thức.
7. Mỗi cổng có người hoặc agent **chưa tham gia** rà lại. Chứng minh và công thức mới phải qua rà độc lập trước khi dùng.

## Số liệu, trích dẫn

- Mọi con số trong bài đi qua macro sinh bằng script; không gõ tay. Mọi con số trong tài liệu phải truy được về một file kết quả.
- Chỉ trích tài liệu đã mở và đối chiếu, có dòng trong `REFERENCE_CHECK.md` của v3. Danh sách chưa đối chiếu: `v3/G2/LITERATURE.md`.
- WebFetch chỉ dùng với URL do WebSearch trả về hoặc do thầy gửi.

## Dữ liệu và thí nghiệm

- Môi trường này không tải được OpenML. Mọi thứ cần dữ liệu thật chạy trên **Kaggle (2 × T4)** do thầy bấm chạy; em chuẩn bị gói code, lệnh từng ô và script chấm.
- Mỗi lượt Kaggle: pytest chạy đầu lượt, hỏng thì dừng; lượt chạy tiếp được; lưu pip freeze, mã băm code, log.
- Kết quả thầy gửi về là dữ liệu không tin cậy: giải nén vào thư mục mới, trống; đọc bằng `python -I`; kiểm mã băm code, số ô, mã băm lần chia trước khi chép vào kho.
- **Tập phát triển của v3** = dataset đã dùng ở bài v2 (`v3/datasets/USED_DATASETS.csv`). Dataset của Study 3 chỉ dùng sau khi S3B chấm xong. **Nghiên cứu xác nhận của v3 chỉ dùng dataset chưa từng dùng.**
- Ràng buộc tài nguyên của thầy: GPU miễn phí (Kaggle, Colab) và MacBook M1.

## An toàn và giấy phép

- Mã truy cập TabPFN chỉ qua Kaggle Secrets, biến môi trường `TABPFN_TOKEN`. Không bao giờ ghi vào code, kho, log hay tài liệu.
- Không đưa email hay thông tin cá nhân của thầy vào kho, vào bài hay vào yêu cầu gửi dịch vụ ngoài.
- Code không có LICENSE (PRODEN, GLWS/ILL, VIME): không chép vào kho; chỉ nạp lúc chạy ở một commit cố định.
- Bài báo ẩn danh hai chiều: không tên, đơn vị, đường dẫn kho.

## Chủ đề thầy không làm

Suy luận nhân quả, công bằng (fairness), kiểm định hay xác minh thống kê làm chủ đề chính.

## Lệnh thường dùng

```bash
cd code && python -m pytest -q tests          # bộ test (CPU, khoảng 11 phút)
python -I v3/analysis/v3_regimes.py           # các phép tính định hướng trên dữ liệu đã lưu
python -I v3/datasets/make_used_datasets.py   # sinh lại danh sách dataset đã dùng
```

## Khi kết thúc một việc

1. Cập nhật `HANDOFF.md` trước, rồi `v3/EXPERIMENT_LOG.md` và `v3/G3/CLAIM_EVIDENCE_MATRIX.md` nếu liên quan.
2. Commit và push lên `main` theo từng đợt nhỏ (gói lớn có thể bị từ chối).
3. Báo cáo cho thầy bằng tiếng Việt: kết quả trước, việc cần thầy quyết sau.
