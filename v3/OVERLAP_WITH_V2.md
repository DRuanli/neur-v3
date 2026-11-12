# Ranh giới giữa bài v2 và bài v3

*Ngày 12/11/2026. Căn cứ: quy tắc 11 của sổ tay (không tự đạo văn, không chia nhỏ một kết quả thành nhiều bài, không nộp song song).*

| | Bài v2 | Bài v3 |
|---|---|---|
| Kho | `DRuanli/icgibbs` | `DRuanli/neur-v3` |
| Đích | một tạp chí (thầy chọn) | NeurIPS 2027 |
| Câu hỏi | phương pháp In-Context Gibbs có hơn baseline không, và vì sao chuỗi có lúc hỏng | một nhãn yếu đáng bao nhiêu nhãn thật với một TFM đóng băng; trần ở đâu |
| Đóng góp | phương pháp (một chuỗi, nhiều điểm xuất phát, nhiều TFM); Định lý 1–3; Study 1–3; S3B | thước đo tỉ giá; tỉ giá trần; sơ đồ vùng; quy tắc không cần nhãn; các loại nhãn yếu mới; Study 4 |

## Bài v3 được làm gì với nội dung của v2

- **Trích** bài v2 cho phương pháp, Định lý 1–3 và kết quả Study 1–3. Trong bài v3 phương pháp được mô tả gọn, có trích dẫn, không trình bày như đóng góp mới.
- **Dùng lại code** (thư viện `icgibbs`): là công cụ, không phải đóng góp.
- **Dùng dataset của Study 1–3 làm tập phát triển.** Không dùng chúng trong nghiên cứu xác nhận của v3.
- **Phân tích lại số liệu của Study 1–3** như phân tích thăm dò có ghi nguồn (ví dụ R-A đến R-E). Chúng chỉ được dùng để tạo giả thuyết.

## Bài v3 không được làm gì

- Không báo cáo lại Study 1–3 như kết quả mới, không chép bảng hay hình của v2.
- Không chép nguyên văn đoạn nào của v2. Phần phương pháp và phần liên quan viết lại.
- Không dùng một dataset cho nghiên cứu xác nhận của cả hai bài.
- Không nộp v3 khi nội dung chính của nó còn nằm trong một bản thảo v2 đang được phản biện mà không khai báo quan hệ giữa hai bài.

## Việc phải làm khi nộp

- Khai báo trong thư gửi (và trong bài, theo quy định ẩn danh của hội nghị) rằng có một bài liên quan của cùng nhóm, và nêu khác biệt.
- Nếu v2 chưa công khai lúc nộp v3: trích dạng ẩn danh và gửi bản v2 ẩn danh làm tài liệu bổ sung, theo quy định của NeurIPS 2027 về công trình đồng thời của cùng tác giả (phải kiểm khi có thông báo gọi bài).

## Kết quả thuộc về bài nào

| Kết quả | Thuộc |
|---|---|
| S3B / S3BC (đang chờ chạy) | v2. Bài v3 chỉ dùng cho mốc M1 và trích lại |
| H-A, H-B, R-A đến R-E | v3, mức thăm dò, trên dữ liệu của v2 |
| Hai công thức tín hiệu yếu | v3 |
| Quan sát "túi gom theo feature dễ hơn" (V1C) | đo ở v2; lời giải thích bằng công thức thuộc v3 |
