# Ma trận khẳng định – bằng chứng của bài v3

*Khởi tạo 12/11/2026. Cập nhật mỗi khi một mốc xong. Một khẳng định chỉ được viết vào bài khi cột "Bằng chứng xác nhận" có nội dung; bằng chứng thăm dò chỉ dùng để quyết định có theo đuổi hay không.*

| Mã | Khẳng định (dạng sẽ viết) | Loại | Bằng chứng thăm dò | Bằng chứng xác nhận | Trạng thái |
|---|---|---|---|---|---|
| C1 | Tỉ giá quy đổi của PLL và LLP dưới một TFM đóng băng nằm trong khoảng …, giảm theo mức nhãn yếu và tăng theo độ tách lớp | thực nghiệm | R-E: 6 dataset, TabPFN v2 (`results/v3_exchange_rate.csv`) | — | chưa viết được |
| C2 | Tỉ giá trần ở tín hiệu yếu là ρ_b + (1 − ρ_b)/m cho LLP và (E[1/\|S\|] − 1/C)/(1 − 1/C) cho PLL; ở tín hiệu hữu hạn là … | lý thuyết | chứng minh nháp và kiểm số (`THEORY_NOTES.md` §1) | chứng minh đã rà độc lập: — | chưa viết được |
| C3 | Ở vùng dễ, bộ lấy mẫu đạt tỉ giá gần trần; baseline huấn luyện đạt thấp hơn | thực nghiệm | một điểm: 0,38 so với 0,388 | — | chưa viết được |
| C4 | Có một vùng mà kết quả phụ thuộc điểm xuất phát dù thông tin đủ | thực nghiệm + lý thuyết | Study 3 của v2: 39% ô PLL khác lưu vực | — | chưa viết được |
| C5 | Tỉ giá và vùng dự báo được từ đại lượng không cần nhãn | thực nghiệm | V1C của v2: túi gom theo feature dễ hơn (giải thích sau sự kiện) | — | chưa viết được |
| C6 | Khung đo và bộ lấy mẫu áp dụng cho nhãn bù, MIL, số đếm có nhiễu và dữ liệu nhãn yếu thật | thực nghiệm | PLL thật 3 bộ ở Study 1 của v2 | — | chưa viết được |

## Khẳng định KHÔNG được viết (đã có bằng chứng ngược)

| Khẳng định | Bằng chứng ngược |
|---|---|
| "Nhãn yếu gần như miễn phí với TFM" | R-E: tỉ giá dưới 0,13 ở phoneme |
| "Phương pháp không cần huấn luyện" | khởi động ấm của LLP huấn luyện một DLLP tuyến tính; điểm xuất phát L là một learner đã tune |
| "Chuỗi giúp ở mọi loại nhãn yếu" | R-A: âm ở nhãn nhiễu và bán giám sát |
| "Chẩn đoán được chuỗi hỏng mà không cần nhãn" | H8 và H3″ của v2 đều trượt |
| "Định lý 3 dự báo được lưu vực trên dữ liệu thật" | cần biên 0,25–0,35, đo được ≤ 0,14 |
