# Những gì đã biết khi bắt đầu bài v3 (tổng hợp ngày 12/11/2026; cập nhật 13/11/2026 với S3B)

Tài liệu này gom mọi phát hiện của bài v1/v2 mà bài v3 cần, kèm nơi lấy số. Bản chụp đầy đủ của dự án cũ nằm ở `prior/` (commit `120c4d9` của kho `icgibbs`). Khi một con số ở đây lệch với file nguồn, **file nguồn đúng**.

Ký hiệu độ tin cậy:
- **[XN]** kết quả xác nhận: giả thuyết, dataset và script chấm ghi trước khi chạy.
- **[TD]** thăm dò: phân tích sau sự kiện hoặc chạy trên tập phát triển. Không dùng làm khẳng định trong bài.
- **[LT]** lý thuyết có chứng minh đã qua rà độc lập. **[LT-nháp]** chưa rà.

## 1. Phương pháp đang có

**In-Context Gibbs.** Dưới prior trao đổi được, dự đoán của TFM cho một điểm khi biết nhãn các điểm còn lại chính là xác suất có điều kiện đầy đủ của một bộ lấy mẫu Gibbs trên nhãn ẩn. Nhãn yếu đi vào qua hàm hợp lý: tập ứng viên cho PLL, số đếm của túi (quy hoạch động) cho LLP. TFM không được huấn luyện lại.

| Thành phần | Cấu hình |
|---|---|
| Một chuỗi (v1) | 10 khối, 30 vòng quét, bỏ 10 vòng đầu, trung bình trên 10 mẫu, ngữ cảnh tối đa 2.000 điểm; khoảng 310 lần gọi TFM |
| Khởi động ấm | PLL: TFM ngây thơ cross-fit. LLP: DLLP tuyến tính (có huấn luyện một mô hình tuyến tính) |
| Nhiều điểm xuất phát (A1) | trung bình đều ba chuỗi: ấm, từ learner L, lạnh. L là DLLP-MLP đã tune (LLP) hoặc CC đã tune (PLL) |
| Nhiều TFM (X) | trung bình đều A1 trên TabICL v2, TabPFN-3, TabDPT, TabPFN v2 |

Code: `code/icgibbs/` (bản sống) và `prior/G4/code/` (bản đóng băng). Đặc tả: `prior/G4/METHOD_SPEC.md`.

## 2. Kết quả xác nhận

### Study 1 [XN] — TabPFN v2, 24 dataset OpenML-CC18 (10 nhị phân, 14 đa lớp)

| Giả thuyết | Kết quả |
|---|---|
| H2, LLP túi 8, so đối thủ chính | +0,024 AUC, 8/0/2, p = 0,232: **không đạt** |
| H4, PLL q 0,3 | +0,022, p = 0,084: không đạt |
| H4, PLL q 0,6 | −0,132, 7/0/7: **không đạt**; chuỗi sụp ở dataset từ 8 lớp |
| H3, Gibbs hơn hard-EM | 86,7% của 128 ô: đạt |
| H5, PLL thật (BirdSong, Lost, MSRCv2) | hạng trung bình 2,15, đứng đầu 10 phương pháp: đạt |

Nguồn: `prior/G8/G8_REPORT.md`, `prior/G8/results/`.

### Study 2 [XN] — TabICL v2, 28 dataset mới (18 nhị phân, 10 đa lớp)

| Giả thuyết | Kết quả |
|---|---|
| H2′, LLP túi 8, so DLLP tuyến tính | +0,052 AUC [+0,024; +0,086], 16/0/2, p_Holm < 0,001 |
| H4′, PLL so CC tune | +0,012 ở cả q 0,3 và q 0,6, p = 0,016 |
| H3′ | 78,9% của 38 ô |

- So với baseline mạnh nhất ở LLP (DLLP-MLP tune): +0,041, 16/18.
- H4′ ở q 0,6 nhạy với nhiễu Monte Carlo: chuỗi thứ hai cho p_Holm 0,074.

Nguồn: `prior/S2/S2_RESULTS.md`, `prior/S2/results/`.

### Study 3 [XN] — 4 TFM, 20 dataset mới, LLP túi 8 và PLL q 0,6, 71 cặp (TFM, dataset)

| Giả thuyết | Kết quả |
|---|---|
| H1″, A1 hơn một chuỗi | +0,058 [+0,016; +0,114], 13/6/1, p_Holm 0,0004. Trung vị chỉ +0,003; lợi dồn ở PLL (+0,136), LLP +0,007 |
| H2″, X hơn A1 của một TFM | +0,046, 18/2/0, p < 0,001 |
| H3″, chẩn đoán không cần nhãn | AUC 0,766: **không đạt** |
| C4″, tỉ lệ thụt lùi | 10/71 = 14,1%: **không đạt** (9 trong 10 là kém learner L) |
| C5″ | đạt |
| A1 so với L | +0,018, p = 0,14: không có ý nghĩa |

Nguồn: `prior/S3/S3_REPORT.md`, `prior/S3/results/s3_summary.json`, dự đoán từng chuỗi ở `prior/S3/raw/S3/s3_npz/` (213 file).

## 3. Phát hiện thăm dò quan trọng cho v3

### 3.1 Trên Study 3 [TD] (`prior/S3/s3_explore.py`)

- X hơn L ở **20/20 dataset** (+0,064 [+0,030; +0,110]).
- Lợi của nhiều điểm xuất phát đến từ **điểm xuất phát learner**: chuỗi từ L một mình gần bằng A1 (+0,001); chuỗi lạnh không thêm gì.
- Bỏ TabICL v2 khỏi X thì mất 0,028; bỏ TFM nào khác thì mất không quá 0,001. X không hơn có ý nghĩa so với riêng A1 của TabICL v2 (+0,016, p 0,08).
- **Kết quả phụ thuộc điểm xuất phát chủ yếu ở PLL:** ba chuỗi về cùng một lưu vực ở 91% ô LLP nhưng chỉ 61% ô PLL. Khi các chuỗi khác lưu vực, lợi của A1 ở PLL là +0,328; khi cùng lưu vực là +0,006.
- Ví dụ rõ nhất, PLL q 0,6 với TabPFN-3: chuỗi ấm 0,371, chuỗi từ learner 0,692.
- Chi phí một chuỗi trên T4: trung vị 92 giây (TabICL v2), 120 (TabDPT), 172 (TabPFN-3), 208 (TabPFN v2). X mất trung vị 37 phút mỗi ô.

### 3.2 Cơ chế [TD]

- **Ánh xạ phản ứng** (độ đúng của nhãn TFM gán lại, theo độ đúng của ngữ cảnh): TabPFN v2 củng cố nhãn ngữ cảnh sai trong một vùng; TabICL v2 thì không (`prior/S2/S2X_REPORT.md`).
- Ánh xạ đo bằng nhiễu đều **không dự báo** được điểm dừng của chuỗi: chuỗi dừng cao hơn điểm bất động của nó ở 96% trong 234 ô (sai số trung vị 0,073). Ánh xạ đo trên chính trạng thái của chuỗi thì khớp (sai số 0,016), nhưng đó là phép đo vòng tròn, không phải dự báo (`prior/V2/V1C_REPORT.md`).
- Chuỗi chạy 30 vòng quét hay dài hơn: S3B (mục 3.4) cho thấy 100 vòng hiếm khi sửa được ô kẹt, nhưng chuỗi TabPFN-3 leo chậm; kẹt là lẫn giữa lưu vực và trộn chậm.
- Khối có sửa Metropolis–Hastings: chậm hơn trung vị 7 lần, không tốt hơn ở PLL (`prior/S2/S2E_REPORT.md`).
- Túi gom theo feature **dễ hơn** túi ngẫu nhiên, trái với giả định lúc thiết kế (`prior/V2/V1C_REPORT.md` §8). Xem `THEORY_NOTES.md` §1.1 để có lời giải thích.

### 3.3 Định hướng cho v3 [TD] (`v3/analysis/`, chạy ngày 12/11/2026 trên bảng đã lưu)

| Mã | Phép tính | Kết quả | Hệ quả |
|---|---|---|---|
| H-A | Trần của việc chọn chuỗi ở Study 3 | bộ chọn hoàn hảo chỉ hơn X +0,011 | bỏ hướng chẩn đoán và chọn chuỗi |
| H-B | Phần khoảng cách naive → oracle mà một chuỗi lấy lại, Study 2 | LLP túi 8: 75%; PLL q 0,3: 73%; q 0,6: 91% | phương pháp đã gần trần theo thước đo này |
| R-A | Như H-B, Study 1 (TabPFN v2), mọi loại nhãn yếu | LLP túi 8 / 16 / 32: 68% / 67% / 60%. PLL q 0,3: 86%; q 0,6: 47%. Nhãn nhiễu, bán giám sát: **âm**. PU-SAR: 4% và 15% | chuỗi chỉ có ích ở nơi hàm hợp lý của nhãn yếu mang thông tin mà nhãn ngây thơ không có (PLL, LLP), đúng như Mệnh đề về TFM ngây thơ |
| R-C | Phần lấy lại là tính chất của dataset hay của mức nhãn yếu | LLP: tương quan hạng giữa các cỡ túi 0,83 đến 0,93. PLL với TabPFN v2: −0,33 (các dataset nhiều lớp chuyển từ dễ ở q 0,3 sang hỏng ở q 0,6) | ở LLP độ khó gắn với dataset; ở PLL có chuyển tiếp theo q |
| R-D | LLP: chuỗi so với điểm xuất phát và so với AUC của oracle | chuỗi hơn điểm xuất phát ở 37/48 cặp, kể cả khi điểm xuất phát tệ hơn TFM ngây thơ (từ −0,16 lên 0,44). Phần lấy lại tăng theo AUC của oracle: 0,25 / 0,53 / 0,70 / 0,79 ở bốn khoảng AUC | ở LLP điểm xuất phát không quyết định; độ tách lớp mới quyết định |
| R-E | **Tỉ giá quy đổi** n_eff/n từ ablation cỡ dữ liệu của Study 1 | từ dưới 0,13 (phoneme) tới 0,8 (sick); tăng theo độ tách lớp; trùng dự báo tín hiệu yếu ở dataset khó nhất của PLL (0,38 so với 0,388) | đổi thước đo chính của v3 sang tỉ giá; xem `THEORY_NOTES.md` |

Số đầy đủ: `v3/results/v3_headroom.txt`, `v3/results/v3_regimes.txt`.

**Cảnh báo về thước đo.** "Lấy lại 75% khoảng cách" và "tỉ giá 0,13" có thể cùng đúng trên một dataset. Đường học của TFM có nhãn thật rất phẳng, nên một khoảng cách nhỏ về AUC ứng với rất nhiều nhãn. Bài v3 phải báo cáo cả hai và lấy tỉ giá làm chính.

### 3.4 Lượt bổ sung S3B / S3BC của bài v2 (13/11/2026) — B1, B2 chính thức; B3 tạm thời

Báo cáo đầy đủ: `prior/S3/S3B_REPORT.md`. Dữ liệu: `prior/S3/raw/S3B/`. Kiểm định luận điểm v3 bằng các số này: `V3_IDEA_CHECK_2026-11-13.md`.

| Mã | Kết quả | Loại |
|---|---|---|
| B1 | X hơn GBDT tự huấn luyện không tune +0,135 (trung vị +0,031), 19/0/1, p_Holm 0,0002; hơn PL-kNN không tune +0,188, 8/0/0, p_Holm 0,016 | [XN-bổ sung] |
| B1 | L (đã tune) so với baseline CPU tốt hơn: +0,022, trung vị −0,003, 7/1/12, p 0,84 | [XN-bổ sung] |
| B1 | Chuỗi đơn − GBDT: +0,031 [−0,003; +0,071], 11/1/8. Ở PLL, trung bình chuỗi đơn 0,589 thấp hơn PL-kNN 0,620 | mô tả |
| B2 | Chuỗi đơn tốt hơn hard-EM về log loss 17/20, p < 0,001; về chỉ số chính +0,020 (LLP +0,001) | [XN-bổ sung] / mô tả |
| B2 | X kém oracle tốt nhất 0,085 (LLP 0,052; PLL 0,135), ở 18/20 dataset | mô tả |
| B2 | TabPFN-3, PLL: chuỗi đơn 0,371 và hard-EM 0,367, sát mức ngây thơ 0,357; A1 0,650 | mô tả |
| B3 | P22 ĐÚNG tạm thời (chỉ TabDPT đủ ô). Xem tạm 67/72 ô: sửa được 5/35 ô kẹt (14%), nhưng lợi trung bình +0,056; vế "lợi dưới 0,03" sẽ sai khi đủ ô | tạm thời |
| B3 | TabPFN-3 leo chậm: độ đúng nhãn 0,35 → 0,45 từ vòng 30 tới vòng 100, 10/22 ô còn đang tăng | xem tạm |

[XN-bổ sung] nghĩa là kiểm định ghi trước, nhưng ghi **sau** khi Study 3 đã chấm trên cùng dataset.

## 4. Lý thuyết đang có

| Kết quả | Trạng thái | Nguồn |
|---|---|---|
| Bổ đề 1; Định lý 1 (tính đúng với PPD chính xác) | [LT] | `prior/G4/PROOFS.md`, `prior/paper/sections/appendix_proofs.tex` |
| Định lý 2 (độ bền dưới TFM xấp xỉ) | [LT]; dạng cận là kinh điển, và **rỗng** với khối không sửa | như trên |
| Định lý 3 (sàn, trần, lưu vực) dưới Giả định phản ứng đồng nhất | [LT]; **không chứng nhận được gì ở cỡ dataset hiện có** (cần biên 0,25–0,35, đo được ≤ 0,14); độ lệch δ của giả định chưa ước lượng; không phủ LLP | `prior/V2/W1_R1A_REPORT.md` |
| Mô-men dừng; độ lệch dự đoán của khối không sửa | [LT], trong mô hình liên hợp | như trên |
| Mệnh đề về TFM ngây thơ (khi nào nhãn ngây thơ đã đủ) | [LT]; đã sửa một lỗi cũ về thông tin Fisher của LLP | `appendix_proofs.tex` |
| Tỉ giá trần ở tín hiệu yếu | **[LT-nháp]**, 12/11. Phần LLP đã có trong tài liệu; không dự báo được kết quả ở dữ liệu thật (13/11) | `v3/THEORY_NOTES.md` |

## 5. Kết quả âm và dự đoán sai (giữ lại, đừng lặp lại)

- 7 trong 17 dự đoán ghi trước ở giai đoạn phát triển của v2 **sai** (bảng đầy đủ ở phụ lục bài v2, `tab:devpred`).
- Chẩn đoán không cần nhãn để biết chuỗi nào hỏng: thất bại hai lần (H8, H3″).
- Điểm khớp nhãn yếu (WPLL) chọn đúng chuỗi ở PLL trên tập phát triển nhưng không ở LLP, và ở Study 3 không hơn việc gộp đều.
- Trộn hai TFM trong cùng một bộ lấy mẫu: cần 35–85% trọng số của TFM tốt mới thoát vùng xấu.
- Chuỗi lạnh không đóng góp.
- Bối cảnh "khó" thiết kế bằng túi gom theo feature hoá ra dễ hơn.
- Với nhãn nhiễu, bán giám sát và PU, chuỗi không hơn TFM ngây thơ.
- (13/11) "Phần lấy lại tăng theo AUC của oracle" (R-D) không lặp lại trên dữ liệu mới của S3B: ρ = +0,18.
- (13/11) Dự báo "vùng bất khả" theo η_low·n sai trên hai dataset (1515, 42).
- (13/11) Chuỗi đơn không hơn rõ một GBDT không tune; ở PLL thua PL-kNN không tune về trung bình.

## 6. Bốn vòng phản biện bài v2 nói gì

Điểm kiểu NeurIPS: vòng 1 là 4/10, vòng 2 là 5/10 (Soundness 3, Presentation 2, Contribution 3). Biên bản ở `prior/G9/reviews/`, cách xử lý ở `prior/G9/REVIEW_V2_RESPONSE.md`.

Điểm yếu còn lại là điểm yếu khoa học, không sửa bằng viết lại được:
1. Study 3 chỉ có một baseline (L). Đã bổ sung bằng S3B: X hơn GBDT và PL-kNN không tune; nhưng chuỗi đơn thì không hơn rõ.
2. Cấu hình khuyến nghị (X) chỉ hơn L trong phân tích thăm dò.
3. Định lý 3 không định lượng được ở cỡ dữ liệu thật.
4. Lợi ích trung vị nhỏ; lợi dồn vào PLL nhiều lớp.
5. Không có LLP thật; PLL thật chỉ 3 bộ.

Các lỗi lặp lại mà phản biện bắt được (đã thành quy tắc ở sổ tay chương 11): nói quá phạm vi của định lý; gọi "không huấn luyện" khi khởi động ấm có huấn luyện; số gõ tay lệch số sinh từ script; bảng dự đoán thiếu các dự đoán sai; quy tắc tính hoà không nhất quán giữa các study.

## 7. Việc còn treo từ dự án cũ

- **S3B / S3BC:** đã chạy và chấm ngày 13/11 (mục 3.4). Còn 5/72 ô B3 cần một phiên Kaggle nữa (chạy tiếp được); chấm B3 lần cuối ở kho `icgibbs` rồi chép sang `prior/`.
- Bài v2 ở bản nháp 3, sẽ gửi tạp chí. Ranh giới giữa hai bài: `v3/OVERLAP_WITH_V2.md`.

## 8. Dataset

- 83 dataset OpenML đã dùng hoặc đã nêu tên: `v3/datasets/USED_DATASETS.csv`. Thêm 3 bộ PLL thật (BirdSong, Lost, MSRCv2).
- Mọi dataset đã dùng đều dùng được làm **tập phát triển** của v3. Riêng 20 dataset của Study 3 chỉ dùng sau khi B3 của S3B chấm xong (còn 5 ô).
- **Nguồn dataset mới sắp cạn.** Lần đếm cho Study 3 (9 suite OpenML, 267 dataset) có 43 ứng viên ở bậc tiêu chí rộng nhất; 20 đã dùng, 23 còn lại đều đã bị loại khi rà tay (`prior/S3/s3_review.csv`). Study 4 cần nguồn mới; xem `V3_PLAN.md` §7.
- TabDPT được huấn luyện trên 123 dataset OpenML thật (`prior/V2/data/tabdpt_pretrain_ids.csv`); phải loại chúng khỏi mọi nghiên cứu xác nhận có TabDPT.

## 9. Hạ tầng

- Kaggle 2 × T4, phiên tối đa khoảng 11 giờ; mỗi lượt chạy tiếp được; pytest chạy đầu mỗi lượt.
- Môi trường làm việc này không tải được OpenML: mọi thứ cần dữ liệu thật phải chạy trên Kaggle.
- Mã truy cập TabPFN chỉ qua Kaggle Secrets, biến `TABPFN_TOKEN`.
- Code của PRODEN, GLWS/ILL, VIME không có giấy phép: không chép vào kho, chỉ nạp lúc chạy.
