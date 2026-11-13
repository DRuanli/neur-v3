# Ghi chú lý thuyết của v3: tỉ giá quy đổi nhãn yếu (12/11/2026)

- **Trạng thái:** bản nháp của em, viết ngày 12/11/2026. **Chưa có ai rà độc lập.** Hai công thức ở §1 đã kiểm bằng mô phỏng (`v3/analysis/check_eta_low.py`), nhưng mô phỏng chỉ kiểm phép tính đại số, không kiểm việc công thức có trả lời đúng câu hỏi hay không.
- **Việc bắt buộc trước khi dùng trong bài hay trong một dự báo ghi trước:** một người hoặc agent chưa tham gia rà toàn bộ tài liệu này (quy tắc 10 của sổ tay).
- **Cập nhật 13/11/2026 (`V3_IDEA_CHECK_2026-11-13.md`):**
  - Công thức LLP ở §1.1 đã có dưới dạng số mẫu (Busa-Fekete và cộng sự, ICML 2025: tổng số mẫu tăng tuyến tính theo cỡ túi; Javanmard và cộng sự 2024: phương sai lớn hơn khoảng k lần; PriorBoost 2024: túi chọn có chủ đích tốt hơn túi ngẫu nhiên). Không còn là đóng góp mới.
  - Dự báo "vùng bất khả" ở §5 bị dữ liệu mới bác: hai dataset có η_low·n ≈ 14–16 vẫn được X lấy lại 73% và 87% khoảng cách. η_low chỉ là giới hạn tín hiệu yếu, mà dữ liệu thật xa giới hạn đó.
  - Khuôn mẫu "tỉ giá tăng theo độ tách lớp" (§4) không lặp lại ở dạng phần lấy lại (R-D, ρ = +0,18 trên dữ liệu mới).
  - Vì vậy em **dừng việc rà độc lập** tài liệu này cho tới khi thầy chọn hướng; nó chỉ cần rà nếu chọn hướng A.
- **Tính mới chưa kiểm (ghi ngày 12/11):** nguyên lý nền (thông tin thiếu, mục 2) là kinh điển. Em chưa tra xem hai công thức ở §1 đã được viết ra cho LLP và PLL hay chưa. Xem `G2/LITERATURE.md` mục 4.

## 0. Đại lượng trung tâm

**Tỉ giá quy đổi** của một loại nhãn yếu, với một phương pháp và một TFM:

> η = n_eff / n, trong đó n_eff là số nhãn thật mà chính TFM đó cần (dùng theo cách thông thường) để đạt đúng chỉ số mà phương pháp đạt được trên n điểm nhãn yếu.

- η = 1: nhãn yếu tốt ngang nhãn thật. η = 0,1: mười điểm nhãn yếu đáng một nhãn thật.
- Đo được bằng thực nghiệm: cần đường học của oracle (TFM có nhãn thật ở nhiều cỡ n′), mỗi điểm trên đường là một lần gọi TFM.
- So với thước đo "phần khoảng cách naive → oracle đã lấy lại" (dùng ở `v3_headroom.py`): thước đo đó phụ thuộc vào việc TFM ngây thơ tệ đến đâu và làm kết quả trông đẹp hơn. Ví dụ ở phoneme, LLP túi 8: chuỗi lấy lại 54% khoảng cách, nhưng 3.776 điểm nhãn yếu chỉ đáng chưa tới 500 nhãn thật (η < 0,13). Tỉ giá là thước đo khắt khe và dễ diễn giải hơn, và có lý thuyết đi kèm.

## 1. Tỉ giá trần ở giới hạn tín hiệu yếu

Thiết lập: mô hình tham số p(y | x, β); "tín hiệu yếu" nghĩa là xét thông tin Fisher tại β = 0 (nhãn gần như độc lập với feature). Tỉ giá trần là tỉ số thông tin Fisher về β giữa quan sát nhãn yếu và quan sát nhãn thật. Một ước lượng hiệu quả trên nhãn yếu cần n/η điểm để đạt phương sai của ước lượng trên n nhãn thật.

### 1.1 LLP, túi cỡ m

Mô hình logistic, y_i ~ Bernoulli(σ(a + βᵀx_i)), quan sát số đếm c = Σ_{i∈B} y_i của từng túi B.

- Theo đồng nhất thức Fisher, score của túi theo β bằng kỳ vọng có điều kiện của score đủ nhãn: E[Σ_i (y_i − p_i) x_i | c].
- Tại β = 0 mọi p_i = π và các nhãn trong túi trao đổi được khi biết c, nên E[y_i | c] = c/m. Score của túi là (c − mπ)·x̄_B, với x̄_B là trung bình feature của túi.
- Thông tin của một túi: mπ(1−π)·x̄_B x̄_Bᵀ. Thông tin đủ nhãn của m điểm: π(1−π)·Σ_i x_i x_iᵀ.
- Gọi Σ_b và Σ_w là hiệp phương sai của feature giữa các túi và trong túi (feature đã quy tâm). Khi đó E[m·x̄_B x̄_Bᵀ] = mΣ_b + Σ_w, còn thông tin đủ nhãn là m(Σ_b + Σ_w).

Với feature một chiều, hoặc lấy tỉ số vết:

> **η_low(LLP) = ρ_b + (1 − ρ_b)/m**, với ρ_b là phần phương sai của feature nằm giữa các túi.

- Túi ngẫu nhiên: ρ_b = 0, nên **η_low = 1/m**. Một túi, bất kể cỡ, đáng đúng một nhãn thật khi học hệ số của feature.
- Túi đồng nhất về feature: ρ_b → 1, η_low → 1.
- Hệ số chặn (tần suất lớp) luôn được học với hiệu suất 1.
- ρ_b tính được từ X và cách chia túi, **không cần nhãn**.

### 1.2 PLL, nhiễu đều

Logit đa thức C lớp, tiên nghiệm lớp đều, mỗi nhãn sai vào tập ứng viên S độc lập với xác suất q, nhãn đúng luôn nằm trong S. Khi đó |S| = 1 + Bin(C−1, q).

- Tại β = 0: P(y = k | S) = 1[k ∈ S]/|S|. Score theo hệ số của lớp k là x·(1[k ∈ S]/|S| − 1/C); score đủ nhãn là x·(1[y = k] − 1/C).
- E[1[k ∈ S]/|S|²] = E[1/|S|]/C. Phần ngoài đường chéo cho cùng một hệ số, nên hai ma trận thông tin tỉ lệ với nhau.

> **η_low(PLL) = (E[1/|S|] − 1/C) / (1 − 1/C).**

| C | q | η_low |
|---|---|---|
| 3 | 0,3 | 0,595 |
| 6 | 0,3 | 0,388 |
| 10 | 0,3 | 0,249 |
| 6 | 0,6 | 0,132 |
| 10 | 0,6 | 0,074 |
| 20 | 0,6 | 0,035 |
| 10 | 0,9 | 0,012 |

### 1.3 Kiểm số

`v3/analysis/check_eta_low.py` mô phỏng hiệp phương sai của score tại β = 0 và so với công thức (`v3/results/check_eta_low.txt`): LLP m = 2, 8, 32 cho 0,5008 / 0,1249 / 0,0314 so với 0,5 / 0,125 / 0,0312; PLL sáu cặp (C, q) lệch không quá 0,0004.

## 2. Ngoài giới hạn tín hiệu yếu

- **Nguyên lý thông tin thiếu** (kinh điển trong lý thuyết EM): thông tin quan sát = thông tin đủ − thông tin thiếu, và thông tin thiếu là kỳ vọng của phương sai có điều kiện của score đủ nhãn khi biết quan sát. Nhãn yếu càng xác định nhãn thật (khi kết hợp với feature) thì thông tin thiếu càng nhỏ.
- **Hệ quả định tính:** khi các lớp tách tốt, feature tự khử nhập nhằng, nên tỉ giá trần tăng từ η_low lên gần 1. Tỉ giá trần là hàm tăng theo độ tách lớp. Đây là một phát biểu **cần chứng minh** cho từng mô hình; hiện em chỉ có lập luận và số liệu thăm dò.
- **Việc cần làm (mốc M4):** công thức tỉ giá trần ở tín hiệu hữu hạn cho ít nhất một mô hình giải được (logistic hoặc probit với feature Gauss; hoặc mô hình liên hợp đã dùng ở RQ1 của bài v2), để có đường cong dự báo η*(mức nhãn yếu, độ tách lớp).

## 3. Nối với các kết quả đã có của bài v2

| Kết quả cũ | Vai trò trong khung tỉ giá |
|---|---|
| Định lý 1 (tính đúng với PPD chính xác) | Với TFM là PPD chính xác, bộ lấy mẫu tính đúng dự đoán Bayes dưới prior của TFM, nên đạt tỉ giá tối ưu Bayes dưới prior đó. Khoảng cách giữa tỉ giá đo được và tỉ giá trần đo sai lệch của TFM cộng với việc chuỗi không trộn |
| Định lý 3 (sàn, trần, lưu vực) | Giải thích vì sao tỉ giá đo được có thể thấp hơn trần dù thông tin đủ: chuỗi kẹt trong lưu vực sai. Đây là "vùng khó" |
| Mệnh đề về TFM ngây thơ | Cho tỉ giá của cách dùng ngây thơ so với trần: trong mô hình logistic, hợp lý từng điểm trên nhãn ngây thơ có thông tin Godambe bằng khoảng 3% thông tin của số đếm ở túi 8 (0,134 / 0,060 / 0,033 / 0,017 / 0,009 cho túi 2 / 4 / 8 / 16 / 32); với PLL nhãn ngây thơ giữ 0,24–0,26 thông tin của tập ứng viên ở q 0,3 và 0,06–0,10 ở q 0,6 |
| Quan sát ở V1C: túi gom theo feature dễ hơn túi ngẫu nhiên, "trái giả định ban đầu" | Đúng như công thức §1.1 (ρ_b lớn thì η_low lớn). Đây là giải thích sau sự kiện, không phải dự báo |

## 4. Đối chiếu thăm dò với số liệu đã có

Từ ablation cỡ dữ liệu của Study 1 (TabPFN v2, một chuỗi, 3 dataset mỗi nhóm; `v3/results/v3_exchange_rate.csv`). Đọc ở n ≤ 2.000 để không dính giới hạn ngữ cảnh.

| Bối cảnh | Dataset | Độ tách lớp (chỉ số của oracle ở n = 2.000) | Tỉ giá đo được | η_low |
|---|---|---|---|---|
| LLP túi 8 | phoneme | AUC 0,95 | < 0,25 ở n = 2.000; < 0,13 ở n đầy đủ | 0,125 |
| LLP túi 8 | spambase | AUC 0,99 | 0,34 | 0,125 |
| LLP túi 8 | sick | AUC 1,00 | 0,57 đến 0,81 | 0,125 |
| PLL q 0,3 | first-order-theorem-proving (6 lớp) | accuracy 0,56 | 0,38 | 0,388 |
| PLL q 0,3 | satimage (6 lớp) | accuracy 0,91 | 0,61 đến 0,64 | 0,388 |
| PLL q 0,3 | optdigits (10 lớp) | accuracy 0,99 | 0,69 đến 0,74 | 0,249 |

Đọc bảng này thế nào:
- Tỉ giá đo được nằm ở hoặc trên η_low, và tăng theo độ tách lớp, đúng chiều lý thuyết nói.
- Ở dataset tín hiệu yếu nhất của PLL (first-order-theorem-proving), tỉ giá đo được (0,38) trùng với η_low (0,388).
- **Giới hạn:** 6 dataset, một TFM, một cấu hình chuỗi; em viết công thức và so với bảng trong cùng một ngày; với phoneme chỉ có cận trên. Đây là lý do để thiết kế thí điểm M2, không phải một kết quả.

## 5. Ba vùng, viết lại bằng tỉ giá

| Vùng | Định nghĩa | Dấu hiệu đo được |
|---|---|---|
| Dễ | tỉ giá đo được gần tỉ giá trần, không phụ thuộc điểm xuất phát | ba điểm xuất phát cho cùng kết quả |
| Khó | thông tin đủ (tỉ giá trần cao) nhưng tỉ giá đo được phụ thuộc điểm xuất phát | chuỗi xuất phát từ learner hơn hẳn chuỗi xuất phát không thông tin |
| Bất khả | η*·n nhỏ hơn số nhãn mà TFM cần để vượt mức ngẫu nhiên | mọi điểm xuất phát, kể cả từ nhãn thật rồi chạy tiếp, đều trôi về mức thấp |

Ví dụ định lượng cho vùng bất khả: PLL 10 lớp, q = 0,9 có η_low = 0,012, nên ở tín hiệu yếu 4.000 điểm chỉ đáng khoảng 50 nhãn thật.

## 6. Câu hỏi mở

1. Tỉ giá trần ở tín hiệu hữu hạn (mục 2).
2. Công thức cho nhãn bù, MIL và số đếm có nhiễu.
3. Tỉ giá trần tính theo thông tin Fisher của một mô hình tham số; TFM là phi tham số. Cần một phát biểu đúng cho bối cảnh Bayes (ví dụ theo thông tin tương hỗ giữa nhãn yếu và hàm cần học), hoặc nói rõ đây là mô hình tham chiếu.
4. Chỉ số dùng để định nghĩa n_eff (AUC, accuracy, log loss) cho các tỉ giá khác nhau; cần chọn trước một chỉ số chính.
5. Đường học của oracle phẳng ở n lớn làm n_eff kém ổn định; cần khoảng tin cậy bằng bootstrap và lưới n′ dày hơn ở vùng dốc.
