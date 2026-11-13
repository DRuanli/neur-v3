# Kiểm định luận điểm v3 bằng kết quả S3B và lần tra tài liệu ngày 13/11/2026

- **Đối tượng kiểm:** luận điểm "tỉ giá quy đổi" của `V3_PLAN.md` bản 2 (12/11/2026) và sáu tuyên bố C1–C6.
- **Dữ liệu mới:** lượt S3B / S3BC của bài v2 trên 20 dataset của Study 3, với 4 TFM (`prior/S3/S3B_REPORT.md`). Các số naive, hard-EM, oracle và baseline CPU chưa ai thấy trước 13/11/2026 06:09 UTC. Các khuôn mẫu đem ra kiểm được viết ngày 12/11 trên Study 1–2.
- **Tính chất:** thăm dò. Không có ngưỡng nào được ghi trước cho các phép kiểm ở đây, nên chúng chỉ cho biết khuôn mẫu cũ có lặp lại trên dữ liệu chưa thấy hay không.
- **Script:** `analysis/v3_s3b_check.py`, `analysis/v3_eta_vs_classes.py`. Đầu ra ở `results/`.

## 1. Kết luận

**Luận điểm "tỉ giá quy đổi" ở bản 2 không đủ cho mức 8–10 và nên bỏ làm luận điểm chính.** Bốn lý do, xếp theo mức nặng:

1. **Phần lý thuyết LLP đã có trong tài liệu.** "Một túi đáng khoảng một nhãn" là nội dung của các cận số mẫu đã công bố cho LLP (mục 3).
2. **Dự báo tín hiệu yếu không dự báo được kết quả ở dữ liệu thật.** Hai dataset có η_low·n chỉ 14–16 "nhãn tương đương" (theo §5 của `THEORY_NOTES.md`, thuộc vùng bất khả) lại cho X lấy lại 73% và 87% khoảng cách.
3. **Khuôn mẫu thực nghiệm chính không lặp lại.** "Phần lấy lại tăng theo độ tách lớp" (R-D) cho ρ = +0,18 trên dữ liệu mới.
4. **Ranh giới vùng khó do TFM quyết định, không do nhãn yếu.** Cùng nhãn yếu, cùng dataset, TabICL v2 lấy lại 61% còn TabPFN-3 lấy lại 2%. Vì vậy không thể có quy tắc chỉ dựa vào (loại nhãn yếu, C, q, n).

Điều dữ liệu mới **ủng hộ mạnh** (4 TFM, 20 dataset mới) là một phân đôi khác. Ở LLP túi 8, các phương pháp rất khác nhau dừng ở cùng một mức. Ở PLL q 0,6, kết quả toả rộng và phụ thuộc điểm xuất phát lẫn TFM. Mục 4 nêu ba hướng đi tiếp.

## 2. Từng tuyên bố, trước và sau

| Mã | Tuyên bố (bản 2) | Bằng chứng mới | Trạng thái |
|---|---|---|---|
| C1 | Đo tỉ giá theo mức nhãn yếu, số lớp, cỡ dữ liệu, độ tách lớp, nhiều TFM | S3B không có đường học của oracle nên không đo được tỉ giá | chưa kiểm; vẫn làm được, nhưng tự nó là một bài đo |
| C2 | Tỉ giá trần có dạng đóng | LLP: đã có trong tài liệu. Cả hai công thức chỉ đúng ở tín hiệu yếu, mà dataset thật xa giới hạn đó (K4) | **suy yếu nặng** |
| C3 | Bộ lấy mẫu đạt gần trần, baseline huấn luyện thì không | LLP: chuỗi đơn − hard-EM +0,001; chuỗi đơn − GBDT tự huấn luyện không tune +0,005 (K3). PLL: trung bình chuỗi đơn (0,589) thấp hơn PL-kNN không tune (0,620) | **bị bác ở LLP**; ở PLL chỉ đúng cho X và A1 |
| C4 | Có vùng mà thông tin đủ nhưng kết quả phụ thuộc điểm xuất phát | PLL: A1 − v1 trung bình +0,131, LLP +0,007. Spread giữa các phương pháp: trung vị 0,219 ở PLL, 0,031 ở LLP | **được ủng hộ**; nhưng xem dòng sau |
| C4′ | Vùng khó là do lưu vực (Định lý 3) | B3, xem tạm 67/72 ô: thêm 70 vòng quét chỉ sửa 5/35 ô kẹt, nhưng chuỗi TabPFN-3 leo chậm (độ đúng nhãn 0,35 → 0,45; 10/22 ô còn đang tăng) | **một phần**: lẫn giữa lưu vực và trộn chậm |
| C5 | Quy tắc không cần nhãn dự báo tỉ giá và vùng | R-D không lặp lại (K2). η_low tương quan với spread (ρ = −0,75), nhưng ở Study 3 nó trùng hoàn toàn với số lớp C. Ở Study 1–2, η_low tách 3 lần hỏng tốt hơn C (AUC 0,88 so với 0,76), nhưng TabICL v2 không hỏng lần nào kể cả ở η_low = 0,074 | **bị bác ở dạng "chỉ từ nhãn yếu"**; ranh giới phụ thuộc TFM |
| C6 | Tổng quát sang nhãn bù, MIL, dữ liệu thật | — | chưa kiểm; MIL đã có đối thủ trực tiếp |

## 3. Tra tài liệu (mốc M0b, phần đầu)

Đã mở trang và đọc tóm tắt hoặc phần kết quả chính của các công trình dưới đây. Chưa đối chiếu đủ chi tiết để trích trong bài.

| Công trình | Nội dung liên quan | Hệ quả cho v3 |
|---|---|---|
| Busa-Fekete, Dick, Gentile, Kaplan, Koren, Stemmer, *Nearly Optimal Sample Complexity for Learning with Label Proportions*, ICML 2025 (arXiv 2505.05355) | Tổn thất bình phương: tổng số mẫu cần tăng tuyến tính theo cỡ túi k, có cận dưới khớp trong trường hợp hai giả thuyết; số túi cần gần như không phụ thuộc k. Cải thiện các cận k² và k³ trước đó | "một túi đáng khoảng một nhãn" đã được chứng minh dưới dạng số mẫu. Công thức 1/m của ta chỉ là bản thông tin Fisher ở tín hiệu yếu |
| Javanmard, Chen, Mirrokni, Badanidiyuru, Fu, *Learning from Aggregate Responses: Instance Level versus Bag Level Loss Functions*, arXiv 2401.11081 (2024) | Hồi quy tuyến tính, túi ngẫu nhiên: ước lượng theo túi không chệch nhưng phương sai lớn hơn khoảng k lần; ước lượng theo điểm có chệch nhưng phương sai nhỏ hơn | cùng hệ số k |
| Javanmard, Fahrbach, Mirrokni, *PriorBoost*, arXiv 2402.04987 (2024) | túi được chọn có chủ đích (gom theo dự đoán tiên nghiệm) tốt hơn túi ngẫu nhiên | cùng tinh thần với công thức ρ_b + (1 − ρ_b)/m |
| Castelli và Cover, *The relative value of labeled and unlabeled samples in pattern recognition with an unknown mixing parameter* (IEEE Trans. Inf. Theory, 1996) | khung "một mẫu không nhãn đáng bao nhiêu mẫu có nhãn" | tiền lệ kinh điển của khung tỉ giá |
| Zhu, Shen, Mosbach, Stephan, Klakow, *Weaker Than You Think: A Critical Look at Weakly Supervised Learning* (arXiv 2305.17442) | NLP: vài chục nhãn sạch mỗi lớp xoá phần lớn lợi ích của các phương pháp học nhãn yếu | tiền lệ thực nghiệm của câu hỏi "nhãn yếu đáng bao nhiêu nhãn sạch" |
| Ahfock và McLachlan, *Harmless label noise and informative soft-labels in supervised classification* (arXiv 2104.02872) | Hiệu suất tương đối tiệm cận (Godambe/Fisher) của nhãn đa người gán so với nhãn thật, dạng đóng | tiền lệ của cách tính tỉ giá bằng thông tin Fisher cho một loại nhãn yếu |
| Liu và Dietterich, *Learnability of the Superset Label Learning Problem*, ICML 2014 | số mẫu cần cho PLL theo độ nhập nhằng (chưa đọc được định lý) | phải đọc trước khi nói công thức PLL là mới |

**Đánh giá tính mới sau lần tra này:**
- Khung tỉ giá: có tiền lệ (Castelli và Cover; Zhu và cộng sự; Ahfock và McLachlan).
- Công thức LLP: đã có dưới dạng số mẫu.
- Công thức PLL: có thể mới ở dạng chính xác này, nhưng là hệ quả nhỏ.

Phần thật sự mới chỉ còn "đo tỉ giá với TFM đóng băng". Đó là một đóng góp đo đạc, không phải đột phá.

## 4. Dữ liệu mới thật sự nói gì, và ba hướng đi tiếp

### 4.1 Ba quan sát vững (dữ liệu mới, 4 TFM)

| # | Quan sát | Số |
|---|---|---|
| O1 | **LLP túi 8: các phương pháp rất khác nhau dừng ở cùng một mức.** Gibbs với TFM, hard-EM với TFM và GBDT tự huấn luyện không tune lệch nhau trung bình không quá 0,005 AUC; DLLP-MLP đã tune thấp hơn. Chỉ việc gộp nhiều TFM (X) nâng được mức này | spread trung vị 0,031; X lấy lại 70% khoảng cách, các phương pháp khác 42–57% |
| O2 | **PLL q 0,6: kết quả toả rộng, phụ thuộc điểm xuất phát và phụ thuộc TFM** | spread trung vị 0,219; A1 − v1 +0,131; chuỗi đơn lấy lại 61% với TabICL v2, 49% với TabDPT, 2% với TabPFN-3 |
| O3 | **Vùng khó không chỉ là lưu vực sai: có trộn chậm** | B3 (xem tạm): TabPFN-3 leo từ 0,35 lên 0,45 trong 70 vòng thêm; TabDPT gần như đứng yên |

### 4.2 Ba hướng

| Hướng | Nội dung | Điểm mạnh | Điểm yếu | Ước lượng của em |
|---|---|---|---|---|
| **A. Thu hẹp thành bài đo** | Đo tỉ giá của PLL, LLP với TFM đóng băng; dùng các cận đã có làm mốc tham chiếu | rẻ, chắc chắn ra kết quả; M2 gần như giữ nguyên | đóng góp đo đạc; lý thuyết không mới | hợp tạp chí hoặc TMLR; NeurIPS ≥ 6 khoảng 20–30%, ≥ 8 dưới 5% |
| **B. Hành vi của TFM khi ngữ cảnh có nhãn sai** | Vì sao cùng một tín hiệu yếu mà TabICL v2 thoát còn TabPFN-3 kẹt? Đo một tính chất của TFM, như mức "tin nhãn ngữ cảnh", bằng thăm dò tổng hợp không cần nhãn yếu, rồi dự báo TFM nào kẹt ở đâu | câu hỏi về mô hình nền tảng, đang được quan tâm; O2 là hiện tượng mạnh trên dữ liệu mới | V1C của bài v2 đã thử ánh xạ phản ứng nhiễu đều và **không dự báo được** (sai 96% ô); rủi ro lặp lại thất bại đó | ≥ 6 khoảng 25–35%, ≥ 8 khoảng 5–10% |
| **C. Đánh giá lại học nhãn yếu trên dữ liệu bảng** | Kiểu "Weaker Than You Think" cho dữ liệu bảng: khi learner đủ mạnh, thuật toán nhãn yếu tinh vi còn đáng bao nhiêu? Nhiều thuật toán LLP, PLL, nhiều learner (GBDT, TFM), dữ liệu LLP thật (LLP-Bench), báo cả tỉ giá | O1 là hiện tượng mạnh; L đã tune thua baseline CPU không tune ở 12/20 dataset là kết quả đáng chú ý; hợp hạng mục Datasets and Benchmarks | gần như một đề tài mới; nhiều baseline phải cài; xa đường phương pháp hiện tại | ≥ 6 khoảng 30–40%, ≥ 8 khoảng 5–10% |

Ngoài ba hướng trên còn phương án D: dồn sức cho bài v2 (nay mạnh hơn nhờ S3B) ở một tạp chí tốt, và chọn đề tài NeurIPS 2027 khác hẳn. Còn khoảng 6 tháng tới hạn nộp.

### 4.3 Đề xuất của em

1. **Không chạy M2 theo thiết kế hiện tại.** Nó được thiết kế để kiểm C1–C3 của luận điểm tỉ giá; với kết quả trên, nó chỉ phục vụ hướng A.
2. **Dù chọn hướng nào, trước hết làm xong bài v2 với S3B.** Đây là việc chắc chắn có giá trị, và mọi hướng v3 đều trích nó.
3. Nếu thầy vẫn muốn NeurIPS 8–10 từ dòng nghiên cứu này, em nghiêng về **C hơn B**. O1 là quan sát rẻ nhất để mở rộng và ít phụ thuộc vào một giả định cơ chế đã thất bại một lần. Trước khi cam kết, làm một bài kiểm "giết hay giữ" trong 1–2 tuần:
   - Tra tài liệu theo giao thức: có benchmark LLP/PLL nào trên dữ liệu bảng với GBDT và TFM chưa?
   - Chạy 3–4 thuật toán LLP công bố (DLLP, một phương pháp nhất quán theo túi, một phương pháp dựa trên chọn túi) cùng GBDT và TFM trên tập phát triển hiện có, ở túi 8 và 32. Ghi trước dự đoán "chênh giữa các thuật toán nhỏ hơn chênh giữa các learner".
   - Nếu dự đoán sai, dừng hướng C.
4. **Mức điểm:** em hạ ước lượng. Với mọi hướng, khả năng đạt 8 trở lên ở NeurIPS 2027 nay dưới 10%. Em nói thẳng để thầy cân nhắc phương án D.

## 5. Các phép kiểm (số đầy đủ ở `results/v3_s3b_check.txt`, `results/v3_eta_vs_classes.txt`)

### K1. Phần khoảng cách naive → oracle được lấy lại (mốc M1)

Oracle lấy trung bình trên các TFM đã chạy dataset đó.

| Bối cảnh | v1 | hard-EM | L | baseline CPU tốt nhất | A1 | X | X so với oracle tốt nhất |
|---|---|---|---|---|---|---|---|
| LLP (12 dataset) | 0,53 | 0,52 | 0,42 | 0,50 | 0,57 | 0,70 | 0,68 |
| PLL (8 dataset) | 0,36 | 0,27 | 0,60 | 0,46 | 0,61 | 0,77 | 0,75 |

- Mốc M1 (X lấy lại ít nhất 50% ở ít nhất một bối cảnh): **qua**.
- So với H-B trên Study 2 (chuỗi đơn TabICL v2: 75% ở LLP, 91% ở PLL q 0,6), chuỗi đơn trên Study 3 thấp hơn nhiều, kể cả khi chỉ xét TabICL v2 (56% và 61%).

### K2. Lặp lại R-D: phần lấy lại theo AUC của oracle (LLP, 46 cặp)

| Khoảng AUC oracle | ≤ 0,8 | 0,8–0,9 | 0,9–0,95 | > 0,95 |
|---|---|---|---|---|
| R-D (Study 1–2) | 0,25 | 0,53 | 0,70 | 0,79 |
| S3B (mới) | 0,55 | 0,50 | 0,27 | 0,71 |

ρ = +0,18 trên 46 cặp. Theo từng TFM: TabDPT +0,48, TabICL v2 +0,08, TabPFN v2 −0,10, TabPFN-3 +0,30. **Không lặp lại.**

### K3. Hội tụ hay toả rộng

Spread = max − min của {v1, hard-EM, L, baseline CPU tốt nhất}.

| | Trung vị spread | Trung vị spread / khoảng cách | Dataset có spread < 0,03 |
|---|---|---|---|
| LLP | 0,031 | 0,25 | 5/12 |
| PLL | 0,219 | 0,41 | 2/8 |

LLP, chênh trung bình: v1 − hard-EM +0,001; v1 − GBDT +0,005; L − GBDT −0,013.

### K4. PLL: η_low và độ khó

- Ở Study 3, ρ(η_low, spread) = −0,75 và ρ(η_low, A1 − v1) = −0,73 (trên cặp). Nhưng η_low, C và n trùng nhau: các dataset nhiều lớp đều nhỏ (399–736 điểm).
- Hai dataset có η_low·n ≈ 14–16 (1515, 42) lại cho X lấy lại 73% và 87% khoảng cách.
- Study 1–2 (q 0,3 và 0,6 trên cùng dataset): cả 3 lần hỏng của chuỗi đơn đều ở TabPFN v2 và ở η_low ≤ 0,132 (AUC của η_low 0,88, của C 0,76). Nhưng TabICL v2 không hỏng lần nào, kể cả ở η_low = 0,074.

### K5. B3, xem tạm trên 67/72 ô

Xem `prior/S3/S3B_REPORT.md` §4.
