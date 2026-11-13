# Ma trận khẳng định – bằng chứng của bài v3

## Bản 3 (13/11/2026): hướng thuật toán SCI

| Mã | Khẳng định (dạng sẽ viết) | Bằng chứng thăm dò | Bằng chứng xác nhận | Trạng thái |
|---|---|---|---|---|
| D1 | SCI-FT một lượt đạt ít nhất bằng X ở PLL, với dưới 1% số lần gọi TFM | — | — | chưa có |
| D2 | SCI-FT hơn baseline tốt nhất từng loại nhãn yếu cấp mẫu và trên PLL thật | — | — | chưa có |
| D3 | SCI không phụ thuộc điểm xuất phát | — | — | chưa có |
| D4 | T1, T2 (và T3) có chứng minh đã rà | — | — | chưa có |
| D5 | LLP: SCI đạt mức X với chi phí thấp hơn nhiều, hoặc kết quả âm | — | — | chưa có |
| D6 | Kết quả đứng trên dataset mới, ghi trước | — | — | chưa có |

Động cơ (đã có, từ bài v2, chỉ dùng để giải thích vì sao cần thuật toán mới, trích v2): PLL q 0,6 trên Study 3, chuỗi đơn lấy lại 36% khoảng cách naive → oracle, X 77%; X tốn khoảng 3.700 lần gọi TFM.

---

## Bản 2 (12–13/11/2026, đã bỏ): luận điểm tỉ giá — giữ để tra

*Khởi tạo 12/11/2026. Cập nhật mỗi khi một mốc xong. Một khẳng định chỉ được viết vào bài khi cột "Bằng chứng xác nhận" có nội dung; bằng chứng thăm dò chỉ dùng để quyết định có theo đuổi hay không.*

| Mã | Khẳng định (dạng sẽ viết) | Loại | Bằng chứng thăm dò | Bằng chứng xác nhận | Trạng thái |
|---|---|---|---|---|---|
| C1 | Tỉ giá quy đổi của PLL và LLP dưới một TFM đóng băng nằm trong khoảng …, giảm theo mức nhãn yếu và tăng theo độ tách lớp | thực nghiệm | R-E: 6 dataset, TabPFN v2 (`results/v3_exchange_rate.csv`) | — | chưa viết được |
| C2 | Tỉ giá trần ở tín hiệu yếu là ρ_b + (1 − ρ_b)/m cho LLP và (E[1/\|S\|] − 1/C)/(1 − 1/C) cho PLL; ở tín hiệu hữu hạn là … | lý thuyết | chứng minh nháp và kiểm số (`THEORY_NOTES.md` §1) | chứng minh đã rà độc lập: — | chưa viết được |
| C3 | Ở vùng dễ, bộ lấy mẫu đạt tỉ giá gần trần; baseline huấn luyện đạt thấp hơn | thực nghiệm | một điểm: 0,38 so với 0,388 | — | chưa viết được |
| C4 | Có một vùng mà kết quả phụ thuộc điểm xuất phát dù thông tin đủ | thực nghiệm + lý thuyết | Study 3 của v2: 39% ô PLL khác lưu vực | — | chưa viết được |
| C5 | Tỉ giá và vùng dự báo được từ đại lượng không cần nhãn | thực nghiệm | V1C của v2: túi gom theo feature dễ hơn (giải thích sau sự kiện) | — | chưa viết được |
| C6 | Khung đo và bộ lấy mẫu áp dụng cho nhãn bù, MIL, số đếm có nhiễu và dữ liệu nhãn yếu thật | thực nghiệm | PLL thật 3 bộ ở Study 1 của v2 | — | chưa viết được |

## Cập nhật 13/11/2026 sau S3B (`V3_IDEA_CHECK_2026-11-13.md` §2)

| Mã | Trạng thái mới |
|---|---|
| C1 | chưa kiểm (S3B không có đường học của oracle) |
| C2 | suy yếu nặng: phần LLP đã có trong tài liệu; công thức tín hiệu yếu không dự báo được kết quả ở dữ liệu thật |
| C3 | bị bác ở LLP (chuỗi đơn ≈ hard-EM ≈ GBDT không tune); ở PLL chỉ đúng cho X và A1 |
| C4 | được ủng hộ (PLL: phụ thuộc điểm xuất phát +0,131, LLP +0,007); "lưu vực" chỉ đúng một phần (TabPFN-3 leo chậm) |
| C5 | bị bác ở dạng "chỉ từ nhãn yếu": R-D không lặp lại; ranh giới phụ thuộc TFM |
| C6 | chưa kiểm |

## Khẳng định KHÔNG được viết (đã có bằng chứng ngược)

| Khẳng định | Bằng chứng ngược |
|---|---|
| "Nhãn yếu gần như miễn phí với TFM" | R-E: tỉ giá dưới 0,13 ở phoneme |
| "Phương pháp không cần huấn luyện" | khởi động ấm của LLP huấn luyện một DLLP tuyến tính; điểm xuất phát L là một learner đã tune |
| "Chuỗi giúp ở mọi loại nhãn yếu" | R-A: âm ở nhãn nhiễu và bán giám sát |
| "Chẩn đoán được chuỗi hỏng mà không cần nhãn" | H8 và H3″ của v2 đều trượt |
| "Định lý 3 dự báo được lưu vực trên dữ liệu thật" | cần biên 0,25–0,35, đo được ≤ 0,14 |
| "Một túi đáng một nhãn" như một kết quả mới | Busa-Fekete và cộng sự, ICML 2025 |
| "Vùng bất khả xác định được từ η_low·n" | S3B: 1515 và 42 có η_low·n ≈ 14–16 nhưng X lấy lại 73% và 87% |
| "Phần lấy lại tăng theo độ tách lớp" | S3B: ρ = +0,18 |
| "Chuỗi đơn hơn baseline không nơ-ron" | S3B: +0,031 [−0,003; +0,071]; ở PLL thua PL-kNN về trung bình |
| "Thêm vòng quét không giúp" | S3B (xem tạm): lợi trung bình +0,056; TabPFN-3 leo chậm |
