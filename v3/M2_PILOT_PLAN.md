# Mốc M2: thí điểm tỉ giá quy đổi và sơ đồ vùng

- **Trạng thái: BẢN NHÁP, chưa đóng băng, chưa được thầy duyệt, chưa có code.** Không chạy gì theo tài liệu này cho tới khi (i) M0b xong, (ii) thầy duyệt, (iii) tài liệu và script chấm được commit với ghi chú "đóng băng".
- **Loại:** thăm dò trên tập phát triển. Kết quả của M2 không vào bài như khẳng định; nó chọn lưới, chỉ số và dự báo cho Study 4.

## 1. Câu hỏi

1. Tỉ giá quy đổi đo được có ổn định giữa các seed tới mức xếp hạng được các mức nhãn yếu không?
2. Tỉ giá phụ thuộc thế nào vào mức nhãn yếu, số lớp, cách chia túi và độ tách lớp? Có theo chiều mà `THEORY_NOTES.md` nói không?
3. Vùng mà kết quả phụ thuộc điểm xuất phát nằm ở đâu theo (q, số lớp)?
4. Baseline huấn luyện đạt tỉ giá bao nhiêu trên cùng các ô?

## 2. Dữ liệu

Tập phát triển của v3 = mọi dataset đã dùng ở Study 1 và Study 2 của bài v2 cùng 9 dataset phát triển cũ (`datasets/USED_DATASETS.csv`). Dataset của Study 3 chưa dùng cho tới khi S3B chấm xong.

Quy tắc chọn (áp dụng lúc đóng băng, bằng script, trên số liệu đã lưu):
- **LLP:** 6 dataset nhị phân có n huấn luyện ≥ 2.000 sau loại trùng, chia đều ba mức AUC của oracle đã đo (thấp, giữa, cao), mỗi mức 2 dataset, lấy theo thứ tự ID.
- **PLL:** 6 dataset đa lớp có n huấn luyện ≥ 2.000, gồm 3 dataset dưới 8 lớp và 3 dataset từ 8 lớp, mỗi nhóm trải ba mức accuracy của oracle.

## 3. Lưới

| Yếu tố | Giá trị |
|---|---|
| Cỡ dữ liệu nhãn yếu n | 500; 1.000; 2.000 (lấy mẫu con phân tầng, cùng seed với lần chia) |
| LLP: cỡ túi m | 4; 8; 16; 32; 64 |
| LLP: cách chia túi | ngẫu nhiên; gom theo feature (biến thể `feat` đã có trong code) |
| PLL: q | 0,1; 0,3; 0,5; 0,7; 0,8; 0,9 |
| TFM | TabICL v2; TabPFN-3 |
| Seed | 0, 1, 2 |

Túi 64 với n = 500 chỉ có 7 túi: ô này được chạy nhưng đánh dấu "ít túi" và báo cáo riêng.

## 4. Phương pháp trên mỗi ô

| Nhóm | Phương pháp |
|---|---|
| Mốc | TFM ngây thơ; oracle ở cùng n; **đường học của oracle** ở n′ ∈ {50, 100, 200, 350, 500, 750, 1.000, 1.500, 2.000} |
| Bộ lấy mẫu | một chuỗi khởi động ấm (cấu hình v1); chuỗi xuất phát từ learner L; chuỗi lạnh |
| Dụng cụ đo vùng (không phải phương pháp) | chuỗi xuất phát từ **nhãn thật**: nếu nó trôi xuống thì trạng thái đúng không bền (dấu hiệu vùng bất khả); nếu nó đứng yên còn các chuỗi khác không lên tới thì là vùng khó |
| Baseline huấn luyện (CPU) | baseline nơ-ron đã tune tốt nhất của loại đó (DLLP-MLP; CC); cây tăng cường tự huấn luyện; PL-kNN cho PLL |

## 5. Chỉ số

- **Chính:** tỉ giá η = n_eff/n, n_eff nội suy theo log n′ trên đường học của oracle; AUC cho LLP, accuracy cho PLL. Ngoài khoảng đã chạy thì ghi cận.
- **Phụ:** phần khoảng cách naive → oracle đã lấy lại; chênh giữa các điểm xuất phát; ρ_b (không cần nhãn).

## 6. Dự đoán (viết trước khi chạy; sẽ chấm đúng / sai)

Các ngưỡng dưới đây là đề xuất, chốt khi đóng băng.

| Mã | Dự đoán |
|---|---|
| P-M2-1 | LLP túi ngẫu nhiên: trung vị tỉ giá giảm đơn điệu theo m ở cả hai TFM |
| P-M2-2 | LLP: tương quan hạng giữa tỉ giá và AUC của oracle (theo dataset, ở m = 8, n = 2.000) ≥ 0,5 |
| P-M2-3 | LLP: túi gom theo feature có tỉ giá cao hơn túi ngẫu nhiên cùng m ở ≥ 75% số ô |
| P-M2-4 | LLP: ở hai dataset có AUC oracle thấp nhất, trung vị tỉ giá nằm trong khoảng [η_low/2; 2·η_low], η_low = ρ_b + (1 − ρ_b)/m |
| P-M2-5 | PLL: ở hai dataset có accuracy oracle thấp nhất, trung vị tỉ giá nằm trong khoảng [η_low/2; 2·η_low], η_low = (E[1/\|S\|] − 1/C)/(1 − 1/C) |
| P-M2-6 | PLL: ô có chênh accuracy ≥ 0,05 giữa chuỗi từ L và chuỗi ấm tập trung ở q ≥ 0,6 và số lớp ≥ 8 (≥ 80% số ô như vậy rơi vào vùng đó); LLP có dưới 10% số ô như vậy |
| P-M2-7 | Ở ô có η_low·n < 30, chuỗi xuất phát từ nhãn thật mất ít nhất một nửa lợi thế so với TFM ngây thơ sau 30 vòng quét |
| P-M2-8 | Baseline huấn luyện tốt nhất có trung vị tỉ giá thấp hơn chuỗi tốt nhất ở cả LLP và PLL |

## 7. Điều kiện dừng (từ `V3_PLAN.md`)

- Độ lệch chuẩn giữa các seed của log η lớn hơn chênh lệch log η giữa hai mức nhãn yếu liền kề ở hơn một nửa số dataset: thước đo không dùng được ở dạng này.
- P-M2-2 sai ở cả hai TFM: tỉ giá không gắn với độ tách lớp, lý thuyết ở `THEORY_NOTES.md` không mô tả được dữ liệu.

## 8. Chi phí ước tính

- Chuỗi: LLP 6 × 3 × 5 × 2 × 3 = 540 ô; PLL 6 × 3 × 6 × 3 = 324 ô; mỗi ô 4 chuỗi; hai TFM. Với 92–172 giây mỗi chuỗi ở n lớn (ở n ≤ 2.000 sẽ nhanh hơn), cận trên khoảng 250 giờ GPU. **Quá lớn cho một thí điểm.**
- **Bản rút gọn đề xuất:** n chỉ lấy 2.000 cho mọi mức, thêm n = 500 và 1.000 chỉ ở m = 8 và q = 0,6; túi gom theo feature chỉ ở m ∈ {8; 32}; chuỗi từ nhãn thật chỉ ở hai mức yếu nhất. Còn 306 ô (LLP 162, PLL 144), khoảng 1.000 chuỗi mỗi TFM. Cận trên khoảng 70 giờ GPU cho hai TFM (25 giờ TabICL v2, 47 giờ TabPFN-3), tức 3–4 phiên Kaggle 2 × T4. Nếu cần rẻ hơn: chỉ chạy TabPFN-3 trên PLL, nơi nó cho thấy phụ thuộc điểm xuất phát rõ nhất.
- Đường học của oracle và TFM ngây thơ: mỗi điểm một lần gọi TFM, không đáng kể.
- Baseline CPU: chạy song song trên CPU của cùng phiên.

## 9. Code cần viết trước khi đóng băng

1. `--split v3dev` trong `run_g7.py`: hợp của tập phát triển cũ, Study 1 và Study 2; không dùng được cho Study 3.
2. Mở `--n_train_max` cho mọi mức của LLP và PLL trên `v3dev`; thêm phần `oracle_curve`.
3. Điểm xuất phát `truth` cho `--part v0`, chỉ cho phép trên `v3dev` và ghi rõ trong đầu ra là dụng cụ đo.
4. Lượt `M2` trong một script lượt mới (`run_v3_lot.sh`), chạy tiếp được, pytest ở đầu lượt.
5. `v3/analysis/m2_report.py`: tính tỉ giá, chấm P-M2-1 đến P-M2-8; thử trên dữ liệu giả trước.
6. Test cho từng mục trên.
