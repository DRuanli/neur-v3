# Bài v3: chương trình nghiên cứu

> **Cập nhật 13/11/2026: luận điểm của bản này bị suy yếu nặng và đang chờ thầy chọn hướng mới.** Kết quả S3B và lần tra tài liệu cho thấy (i) phần lý thuyết LLP đã có trong tài liệu, (ii) dự báo tín hiệu yếu không dự báo được kết quả ở dữ liệu thật, (iii) khuôn mẫu "tăng theo độ tách lớp" không lặp lại, (iv) ranh giới vùng khó do TFM quyết định. Chi tiết, ba hướng thay thế và đề xuất: `V3_IDEA_CHECK_2026-11-13.md`. Mốc M1 đã qua (X lấy lại 70% ở LLP, 77% ở PLL). Không chạy M2 theo thiết kế hiện tại.

*Bản 2, ngày 12/11/2026. Bản 1 (cùng ngày, trong kho `icgibbs`, commit `120c4d9`) là đề xuất đầu tiên; bản này thay nó sau quyết định tách bài của thầy và sau ba phép tính định hướng mới (R-A đến R-E).*

- **Quyết định của thầy (12/11/2026):** v3 là một bài riêng, làm ở Project riêng và kho riêng (`DRuanli/neur-v3`). Bài v2 để nguyên và gửi một tạp chí. Mục tiêu của v3: 8–10 điểm ở NeurIPS 2027 (hạn nộp ước 05/2027).
- **Trạng thái:** chưa có thí nghiệm nào của v3 được ghi trước hay chạy. Mọi con số trong tài liệu này là thăm dò trên dữ liệu cũ.
- **Điều em không hứa được:** không ai lập kế hoạch ra được điểm 8–10. Ước lượng chủ quan của em vẫn là khoảng 40–50% đạt mức 6 trở lên và 10–15% đạt mức 8 trở lên. Chương trình này chọn câu hỏi có trần cao nhất em thấy và đặt mốc dừng sớm.

## 1. Luận điểm

> **Một nhãn yếu đáng bao nhiêu nhãn thật đối với một mô hình nền tảng đóng băng?** Bài đo "tỉ giá quy đổi" đó, đưa ra tỉ giá trần do thông tin quyết định, cho thấy một bộ lấy mẫu trong ngữ cảnh đạt gần trần ở một vùng, bị kẹt ở một vùng khác vì lý do thuật toán, và không phương pháp nào làm được gì ở vùng thứ ba.

Bài v2 hỏi "phương pháp có hơn baseline không". Bài v3 hỏi "nhãn yếu đáng giá bao nhiêu, và giới hạn nằm ở thông tin hay ở thuật toán".

**Vì sao đổi từ "nhãn yếu gần như miễn phí" (bản 1) sang "tỉ giá":**
- Phép tính R-E cho thấy câu "gần như miễn phí" không đứng được khi quy ra nhãn thật. Ở phoneme, chuỗi lấy lại 54% khoảng cách naive → oracle, nhưng 3.776 điểm nhãn yếu chỉ đáng chưa tới 500 nhãn thật. Một reviewer vẽ đường học của oracle sẽ thấy ngay.
- Tỉ giá là đại lượng có lý thuyết: tỉ số thông tin Fisher. Em đã có hai công thức dạng đóng ở giới hạn tín hiệu yếu, và số liệu cũ không mâu thuẫn với chúng (`THEORY_NOTES.md`).
- Ba vùng dễ / khó / bất khả của bản 1 được giữ, nhưng nay định nghĩa được bằng số.

**Tên bài tạm:** *What Is a Weak Label Worth? Exchange Rates of Weak Supervision under Frozen Tabular Foundation Models.*

## 2. Sáu tuyên bố cần có

| Mã | Tuyên bố | Đang có | Còn thiếu |
|---|---|---|---|
| C1 | **Đo:** tỉ giá quy đổi của PLL và LLP, theo mức nhãn yếu, số lớp, cỡ dữ liệu và độ tách lớp, trên nhiều TFM | 6 dataset, 1 TFM, 1 mức mỗi loại [TD] | quét có hệ thống (M2), xác nhận (M5) |
| C2 | **Trần:** tỉ giá trần do thông tin quyết định; dạng đóng ở tín hiệu yếu, đường cong ở tín hiệu hữu hạn | hai công thức tín hiệu yếu [LT-nháp] | rà độc lập; tín hiệu hữu hạn (M4) |
| C3 | **Đạt trần:** ở vùng dễ, bộ lấy mẫu đạt tỉ giá gần trần mà không huấn luyện TFM; các baseline huấn luyện thì không | một điểm khớp (0,38 so với 0,388) [TD] | M2, M5; baseline mạnh |
| C4 | **Kẹt:** có vùng mà thông tin đủ nhưng kết quả phụ thuộc điểm xuất phát; lý thuyết lưu vực giải thích | Study 3: 39% ô PLL khác lưu vực [TD]; Định lý 3 [LT] | định vị vùng này theo (q, số lớp); nối với Định lý 3 |
| C5 | **Quy tắc không cần nhãn:** từ (loại nhãn yếu, mức, số lớp, cách chia túi, n) dự báo được tỉ giá và vùng | công thức ρ_b + (1 − ρ_b)/m tính được không cần nhãn [LT-nháp] | kiểm trên dataset mới với dự báo ghi trước |
| C6 | **Tổng quát:** cùng khung đo và cùng bộ lấy mẫu cho nhãn bù, MIL, số đếm có nhiễu, và ít nhất một bộ dữ liệu nhãn yếu thật | PLL thật 3 bộ (Study 1) | cài đặt, thí điểm (M3) |

Một bài mức 8 cần C1, C2, C3 chắc chắn, cộng ít nhất hai trong ba tuyên bố còn lại.

## 3. Các mốc và điều kiện dừng

Gọi là "mốc" (M) để khỏi lẫn với 13 cổng G0–G12 của sổ tay; mỗi mốc vẫn đi qua các cổng tương ứng.

| Mốc | Việc | Chi phí | Dừng hoặc đổi hướng nếu |
|---|---|---|---|
| **M0** | Định hướng trên dữ liệu cũ: H-A, H-B, R-A đến R-E; hai công thức tín hiệu yếu | **xong 12/11** | — |
| **M0b** | Tra tài liệu cho khung tỉ giá và cho hai công thức (`G2/LITERATURE.md` mục 4); rà độc lập `THEORY_NOTES.md` | CPU, 2–3 ngày | công thức và khung đo đã có sẵn cho đúng bối cảnh này: thu hẹp đóng góp về phần đo với TFM |
| **M1** | Dùng kết quả S3B của bài v2: phần khoảng cách naive → oracle mà X lấy lại trên 20 dataset của Study 3 | **xong 13/11: qua** (LLP 70%, PLL 77%) | dưới 50% ở cả LLP và PLL |
| **M2** | Thí điểm tỉ giá và sơ đồ vùng trên tập phát triển (bản nháp: `M2_PILOT_PLAN.md`) | 3–4 phiên Kaggle | tỉ giá đo được không ổn định giữa các seed tới mức không xếp hạng được các mức nhãn yếu; hoặc tỉ giá không tăng theo độ tách lớp |
| **M3** | Tính tổng quát: nhãn bù, MIL, số đếm có nhiễu; một bộ LLP thật | 1–2 phiên | không loại mới nào cho tỉ giá vượt cách dùng ngây thơ |
| **M4** | Lý thuyết: tỉ giá trần ở tín hiệu hữu hạn; vị trí vùng kẹt từ ánh xạ phản ứng; **viết dự báo cho M5 trước khi chạy** | CPU | dự báo lệch có hệ thống trên tập phát triển |
| **M5** | Study 4: nghiên cứu xác nhận ghi trước trên dataset mới | 4–6 phiên | — |
| **M6** | Viết bài; ba vòng phản biện độc lập (toán, kiểm toán số liệu, kiểu NeurIPS) | — | — |

Từ M2 trở đi, mọi thí nghiệm đều ghi trước: kế hoạch, dự đoán và script chấm được commit trước khi chạy.

## 4. Thiết kế thực nghiệm: các nguyên tắc rút từ bốn vòng phản biện của v2

1. **Mốc so sánh kép.** Mọi ô đều có TFM ngây thơ, oracle ở cùng n, và **đường học của oracle** (để tính tỉ giá).
2. **Baseline không chỉ là mạng nơ-ron.** Mỗi loại nhãn yếu có ít nhất một baseline dạng cây và một baseline kNN, cùng baseline đã tune tốt nhất của tài liệu.
3. **Ít nhất ba TFM** từ ba nhóm tác giả khác nhau; kết luận phải đúng với đa số, không chỉ với TFM tốt nhất.
4. **Dữ liệu nhãn yếu thật** cho ít nhất hai loại.
5. **Vùng chuyển tiếp cần nhiều seed** (5–10), vì kết quả từng seed dao động mạnh ở đó.
6. **Mỗi định lý phải có một con số kiểm được** trên dữ liệu thật. Định lý chỉ "mô tả cơ chế" không đủ cho mức 8.
7. **Một quy tắc tính hoà, một định nghĩa "ô", một chỉ số chính** cho cả bài, chọn trước.
8. **Không dựa vào phân tích thăm dò cho tuyên bố chính.** Cấu hình khuyến nghị phải là cấu hình được kiểm xác nhận.

## 5. Hướng đã cân nhắc và loại

| Hướng | Lý do loại |
|---|---|
| Chẩn đoán không cần nhãn, chọn chuỗi | H-A: trần chỉ +0,011; thất bại hai lần ở v2 |
| Khung "giải mã / EXIT chart" làm đóng góp chính | phép so sánh LLP với giải mã đã có trong tài liệu (BP cho LLP) |
| Luận điểm "nhãn yếu gần như miễn phí" | R-E: không đứng được khi quy ra nhãn thật |
| Trộn TFM trong bộ lấy mẫu | cần 35–85% trọng số của TFM tốt |
| Huấn luyện trước một TFM cho nhãn yếu | vượt tài nguyên; đã có người làm cho PU và MIL |
| Lấy mẫu tuần tự (SMC) thay Gibbs | vẫn gặp vấn đề khởi đầu không thông tin |
| Mở rộng sang nhãn nhiễu, bán giám sát, PU làm trọng tâm | R-A: chuỗi không hơn TFM ngây thơ ở các loại này, đúng như lý thuyết nói |

## 6. Rủi ro

| # | Rủi ro | Mức | Cách giảm |
|---|---|---|---|
| 1 | **Tính mới.** Hiệu suất tương đối của dữ liệu thiếu là kinh điển; có thể đã có người viết tỉ giá cho LLP hoặc PLL | cao | M0b trước mọi việc khác. Phần chắc chắn mới là đo với TFM đóng băng và cho thấy bộ lấy mẫu đạt trần |
| 2 | **Nguồn dataset mới sắp cạn** (trong 9 suite đã đếm có 43 ứng viên ở bậc tiêu chí rộng nhất: 20 đã dùng cho Study 3, 23 còn lại đều đã bị loại khi rà tay) | cao | đếm lại với nguồn rộng hơn và tiêu chí ghi trước; thêm dữ liệu nhãn yếu thật; xem §7 |
| 3 | **n_eff kém ổn định** vì đường học của oracle phẳng ở n lớn | trung bình | lưới n′ dày ở vùng dốc; khoảng tin cậy bootstrap; báo cáo cận khi ngoài khoảng |
| 4 | **Giới hạn ngữ cảnh 2.000 điểm** làm lẫn tỉ giá ở n lớn | trung bình | thí điểm ở n ≤ 2.000 trước; với TFM chịu được ngữ cảnh lớn thì bỏ giới hạn |
| 5 | **Tỉ giá trần là của một mô hình tham số**, còn TFM là phi tham số | trung bình | gọi đúng tên là "mô hình tham chiếu"; tìm phát biểu Bayes (M4) |
| 6 | **"Oracle" là TFM có nhãn thật**, không phải giới hạn tuyệt đối | thấp | thêm một mô hình có giám sát đã tune làm mốc thứ hai |
| 7 | **Trùng với bài v2** | trung bình | `OVERLAP_WITH_V2.md`: v3 không dùng Study 1–3 làm đóng góp, trích v2 cho phương pháp |
| 8 | **Chi phí GPU** của quét nhiều mức × nhiều TFM × nhiều seed | trung bình | thí điểm chọn lưới; chuỗi một TFM tốn 92–172 giây |

## 7. Việc chuẩn bị cho Study 4 phải bắt đầu sớm

- **Đếm dataset:** viết tiêu chí trước, rồi đếm trên nguồn rộng hơn 9 suite OpenML đã dùng. Các nguồn cần khảo sát (em chưa kiểm danh sách và giấy phép): toàn bộ OpenML lọc theo metadata, các bộ benchmark bảng lớn công bố gần đây, UCI.
- **Loại:** 83 dataset ở `datasets/USED_DATASETS.csv`, các bộ cùng nguồn với chúng, và mọi dataset trong tập huấn luyện đã công bố của từng TFM.
- **Dữ liệu nhãn yếu thật:** PLL thật đã có 3 bộ; cần tìm LLP thật và MIL chuẩn, kiểm giấy phép.

## 8. Mốc thời gian (nếu các mốc đều qua)

| Thời gian | Việc |
|---|---|
| 11/2026 | M0b; S3B và M1; duyệt và ghi trước M2; chạy M2 |
| 12/2026 | M3; M4; bắt đầu đếm dataset cho Study 4 |
| 01–02/2027 | Ghi trước và chạy Study 4 |
| 03/2027 | Phân tích; bản nháp; ba vòng phản biện |
| 04/2027 | Sửa; style chính thức; giấy phép; checklist; cập nhật tìm kiếm tính mới |
| 05/2027 | Nộp |

## 9. Việc cần thầy quyết

| # | Câu hỏi | Đề xuất của em |
|---|---|---|
| Q1 | Chấp nhận đổi luận điểm từ "ba vùng" sang "tỉ giá quy đổi" (ba vùng thành hệ quả)? | có |
| Q2 | Thứ tự: M0b (tra tài liệu, rà lý thuyết) trước M2? | có; M0b rẻ và có thể đổi hẳn hướng |
| Q3 | Duyệt thiết kế thí điểm M2 ở `M2_PILOT_PLAN.md` | sau M0b |
| Q4 | Bài v2 gửi tạp chí nào, và khi nào (ảnh hưởng cách v3 trích v2)? | gửi sau khi có S3B; v3 trích bản đã nộp hoặc bản arXiv |
