# Tài liệu cho bài v3: đã có, đã thấy, phải tra

*Ngày 12/11/2026. Quy tắc 9 của sổ tay: chỉ trích tài liệu đã mở và đối chiếu. Tài liệu ở mục 2–4 **chưa** qua bước đó; không được đưa vào bài cho tới khi có dòng tương ứng trong `REFERENCE_CHECK.md` của v3.*

## 1. Đã đối chiếu ở dự án cũ (dùng lại được)

- `prior/G9/REFERENCE_CHECK.md`: bảng đối chiếu; `prior/paper/refs.bib`: 39 mục đang trích trong bài v2.
- `prior/G2/`: giao thức tìm kiếm, nhật ký truy vấn, các công trình gần nhất, kết luận tính mới của bài v1 (24/10/2026). Kết luận đó nói về "dùng TFM có sẵn để học từ nhãn yếu bằng suy luận trên nhãn ẩn"; **không phủ** khung tỉ giá của v3.

## 2. Thấy trong lần kiểm tính mới ngày 12/11 (ý tưởng "giải mã"), chưa đối chiếu

| Công trình | Mã | Vì sao liên quan |
|---|---|---|
| Li và cộng sự, *When and How Unlabeled Data Provably Improve In-Context Learning* (NeurIPS 2025) | arXiv 2506.15329; đã trích ở v2 với khoá `unlabeled_icl_theory` | có phần lặp TabPFN với nhãn giả mềm cho bán giám sát: tiền lệ gần nhất của "lặp TFM trên nhãn ẩn" |
| Zhu và Griffiths, iterated in-context learning | arXiv 2406.01860 | lặp học trong ngữ cảnh như một chuỗi Markov lấy mẫu từ prior |
| TabMGP; martingale posterior cho PFN | arXiv 2510.25154; arXiv 2505.11325 | lấy mẫu hậu nghiệm bằng cách tự điền nhãn với TFM |
| Hu và Ghelichi, noise immunity của TabPFN | arXiv 2604.04868; đã trích ở v2 (`noise_immunity`) | vì sao chuỗi không giúp ở nhãn nhiễu |
| Havaldar và cộng sự, belief propagation cho LLP | arXiv 2310.08056 | đã dùng phép so sánh LLP với kiểm tra chẵn lẻ; là lý do loại khung "giải mã" |
| Balakrishnan, Wainwright, Yu, đảm bảo thống kê cho EM | arXiv 1408.2156 | khuôn mẫu "lưu vực hội tụ" cho thuật toán lặp |
| Wu, Yang, Sun 2026, self-training | arXiv 2602.14029 | lý thuyết tự huấn luyện |
| Oymak và Gulcu 2020 | arXiv 2006.11006 | như trên |
| LLP-Bench; Sheldon và cộng sự (ICDM 2017) | — | nguồn dữ liệu LLP thật (quảng cáo, bầu cử); phải kiểm giấy phép |

## 3. Thấy trong lần tìm ngày 12/11 cho khung của v3, chưa đối chiếu

| Công trình | Mã | Mức đã kiểm | Vì sao liên quan |
|---|---|---|---|
| Möllers, Sextro, Hense, Dernbach, Müller, *In-Context Multiple Instance Learning* | arXiv 2606.06458 | đã mở trang arXiv, đọc tóm tắt | huấn luyện trước một mô hình kiểu PFN cho MIL. Là đối thủ trực tiếp của tuyên bố C6 ở MIL, và là ví dụ của con đường "mỗi loại nhãn yếu một mô hình huấn luyện riêng" |
| Ricci-Tersenghi, Semerjian, Zdeborová, *Typology of phase transitions in Bayesian inference problems* | arXiv 1806.11013 | đã mở trang arXiv, đọc tóm tắt | nguồn chuẩn cho các pha dễ / khó trong suy luận Bayes; tóm tắt nói tới khoảng trống tính toán và pha "hybrid-hard" |
| Yu và cộng sự, *On Learning from Label Proportions* | arXiv 1402.5902 | chỉ thấy trong kết quả tìm | phân tích khả năng học của LLP |
| *On the Power of Deep but Naive Partial Label Learning* | arXiv 2010.11600 | chỉ thấy trong kết quả tìm | cách dùng ngây thơ cho PLL |
| *A Mutual Contamination Analysis of Mixed Membership and Partial Label Models* | arXiv 1602.06235 | chỉ thấy trong kết quả tìm | tính định danh của PLL |
| *Active In-Context Learning for Tabular Foundation Models*; *When, Where, How: Active In-Context Learning for TFMs* | arXiv 2603.27385; arXiv 2611.07886 | chỉ thấy trong kết quả tìm | giá trị của một nhãn đối với TFM, từ phía học chủ động |
| In-Context PU | arXiv 2605.05591; đã trích ở v2 (`inctx_pu`) | đã đối chiếu ở v2 | mô hình huấn luyện riêng cho PU |

Kết quả của lần tìm: em **không thấy** công trình nào đo tỉ giá quy đổi nhãn yếu sang nhãn thật với TFM bảng, hay dùng TFM đóng băng cho LLP và PLL ngoài bài v1/v2 của ta. Đây là kết quả của năm truy vấn trong một buổi, chưa phải một lần tìm theo giao thức.

## 4. Phải tra trước mốc M2 (việc của M0b)

Các mục dưới đây em nêu từ kiến thức nền; **tên bài, tác giả và năm đều phải đối chiếu** trước khi viết vào bất kỳ đâu.

| Chủ đề | Cần tìm gì | Vì sao |
|---|---|---|
| Giá trị tương đối của mẫu có nhãn và không nhãn | công trình kinh điển của Castelli và Cover (thập niên 1990) và các bài nối tiếp | tiền lệ trực tiếp của khung "tỉ giá" cho bán giám sát |
| Nguyên lý thông tin thiếu; hiệu suất tương đối của dữ liệu thiếu | Orchard và Woodbury; Louis (1982); Dempster, Laird, Rubin | nền của `THEORY_NOTES.md` §2 |
| Hiệu suất thống kê của LLP | tỉ số thông tin Fisher của số đếm túi; "một túi đáng một nhãn" đã có ai viết chưa | quyết định C2 mới tới đâu |
| Hiệu suất thống kê của PLL | hiệu suất theo kích thước tập ứng viên; công thức (E[1/\|S\|] − 1/C)/(1 − 1/C) đã có chưa | như trên |
| "Nhãn yếu đáng bao nhiêu nhãn mạnh" trong weak supervision và data programming | các phân tích đổi nhãn yếu lấy nhãn sạch | khung đo có thể đã có tên khác |
| Số mẫu hiệu dụng dưới nhãn nhiễu | hệ số kiểu (1 − 2ρ)² | cùng khái niệm cho một loại nhãn yếu khác |
| Pha dễ / khó trên dữ liệu thật | có ai đo phụ thuộc điểm xuất phát như chỉ dấu pha khó ngoài mô hình tổng hợp chưa | định vị C4 |
| TFM và nhãn yếu từ 06/2026 tới nay | arXiv, OpenReview (NeurIPS 2026, ICLR 2027) | bài v1/v2 kết luận tính mới ngày 24/10/2026; phải cập nhật |

Truy vấn gợi ý: `"label proportions" Fisher information efficiency`; `"partial label" "relative efficiency" OR "Fisher information" candidate set`; `"how many" weak labels "worth" labeled`; `"relative value of labeled and unlabeled samples"`; `"missing information principle" weak supervision`; `tabular foundation model "weak" OR "partial label" OR "label proportions" 2026`.
