# 11 · Bài v3: chuẩn của một bài mức 8–10 và bài học từ bài v2

[← Về README](README.md)

Chương này chỉ áp dụng cho bài v3 trong kho này. Nó bổ sung, không thay, các chương 01–10. Khi chương này và một chương khác cùng nói về một việc, áp dụng yêu cầu chặt hơn.

## 1. "Mức 8–10" nghĩa là gì

- "8–10" là cách thầy gọi nhóm bài mạnh nhất của hội nghị (được chấp nhận ở dạng nổi bật), theo thang 10 điểm. **Thang điểm số của NeurIPS 2027 chưa công bố**; hướng dẫn phản biện của NeurIPS 2026 không nêu thang số trên trang hướng dẫn. Phải kiểm lại khi có thông báo gọi bài.
- Hướng dẫn phản biện NeurIPS 2026 chấm theo bốn mặt, và yêu cầu chấm theo **loại đóng góp** mà tác giả chọn (General, Theory, Use-Inspired, Concept & Feasibility, Negative Results):

| Mặt | Câu hỏi của hướng dẫn | Bài v3 trả lời bằng gì |
|---|---|---|
| Quality | bài có vững về kỹ thuật không; khẳng định có được ủng hộ không; tác giả có cẩn trọng và trung thực về điểm mạnh và điểm yếu không | nghiên cứu xác nhận ghi trước; lý thuyết đã rà độc lập; mục giới hạn viết thẳng |
| Clarity | viết rõ, tổ chức tốt, đủ thông tin cho người đọc | một câu hỏi, một đại lượng, một hình chính |
| Significance | kết quả có tác động không; người khác có dùng hay xây tiếp không | thước đo tỉ giá dùng được cho mọi phương pháp nhãn yếu; quy tắc không cần nhãn |
| Originality | có cho hiểu biết mới, làm sâu hiểu biết, hay nêu bật tính chất quan trọng của phương pháp đã có không | đo và giải thích giới hạn của nhãn yếu với TFM đóng băng |

Nguồn: trang *Reviewer Guidelines* của NeurIPS 2026 (neurips.cc/Conferences/2026/ReviewerGuidelines), mở ngày 12/11/2026.

- **Không ai lập kế hoạch ra được điểm 8.** Việc trong tầm tay là loại mọi lý do để bị điểm thấp và chọn câu hỏi có trần cao. Mọi ước lượng xác suất nói với thầy phải kèm lý do.

## 2. Tám điều kiện, mỗi điều có một phép thử

Một bản thảo chưa qua đủ tám phép thử thì chưa nộp vào NeurIPS; cân nhắc hội nghị hoặc tạp chí khác.

| # | Điều kiện | Phép thử |
|---|---|---|
| 1 | **Một câu hỏi nói được trong một dòng**, và người ngoài lĩnh vực hiểu vì sao nó đáng hỏi | đưa tóm tắt cho một agent chưa biết đề tài; nó nhắc lại đúng câu hỏi và kết quả chính sau một lần đọc |
| 2 | **Kết quả chính nằm trong một hình** | che hết chữ trong bài, chỉ để hình 1 và chú thích; kết quả chính vẫn đọc ra được |
| 3 | **Kết quả chính là xác nhận**, không phải thăm dò | mọi câu trong tóm tắt truy được về một giả thuyết ghi trước có ngày commit |
| 4 | **Mỗi định lý chính có một con số kiểm được trên dữ liệu thật** | bảng "dự báo của lý thuyết so với đo được", với dự báo viết trước |
| 5 | **Baseline không thể bị chê**: đủ họ mô hình (nơ-ron, cây, kNN), đã tune cùng ngân sách, tái hiện được số đã công bố | phòng phản biện kiểu NeurIPS không nêu được baseline nào còn thiếu |
| 6 | **Tổng quát**: nhiều TFM, nhiều loại nhãn yếu, dữ liệu nhãn yếu thật | kết luận chính đúng với đa số TFM và ở ít nhất hai loại nhãn yếu |
| 7 | **Giới hạn được nói trước khi reviewer hỏi** | mỗi điểm yếu mà phòng phản biện nêu đã có trong mục giới hạn của bản thảo trước đó |
| 8 | **Tái lập từ bản clone sạch** cho ít nhất một bảng chính | một agent chưa tham gia làm được theo README |

## 3. Mười hai bài học từ bốn vòng phản biện của bài v2

Bài v2 được phòng phản biện kiểu NeurIPS chấm 4/10 rồi 5/10. Các lỗi dưới đây đều đã xảy ra thật; biên bản ở `prior/G9/reviews/`.

| # | Lỗi đã mắc | Quy tắc cho v3 |
|---|---|---|
| L1 | Viện dẫn một định lý cho trường hợp mà một nửa giả định của nó không thoả | trước mỗi câu "theo Định lý X", liệt kê giả định của X và chỉ ra từng giả định được kiểm ở đâu |
| L2 | Định lý "mô tả cơ chế" nhưng hằng số lỏng tới mức không chứng nhận được gì ở cỡ dữ liệu thật | điều kiện 4 ở mục 2; nếu không có con số kiểm được thì định lý xuống phụ lục |
| L3 | Gọi phương pháp là "không huấn luyện" trong khi khởi động ấm có huấn luyện một mô hình | mô tả phương pháp bằng danh sách mọi thứ được fit, kể cả mô hình phụ |
| L4 | Cấu hình khuyến nghị chỉ thắng trong phân tích thăm dò | cấu hình khuyến nghị phải là cấu hình trong giả thuyết xác nhận |
| L5 | Nghiên cứu xác nhận chỉ có một baseline | danh sách baseline là một phần của giao thức đóng băng, và phải qua rà độc lập trước khi đóng băng |
| L6 | Bảng dự đoán bỏ sót các dự đoán sai | bảng dự đoán sinh bằng script từ file dự đoán ghi trước; không lọc |
| L7 | Số gõ tay lệch số sinh từ script | không có số gõ tay trong bài; kiểm toán số liệu độc lập trước mỗi bản nháp gửi đi |
| L8 | Quy tắc tính hoà và định nghĩa "ô" khác nhau giữa các study | một quy tắc cho cả bài, viết ở mục thiết lập chung |
| L9 | So với "baseline mạnh nhất" nhưng thực ra là so với baseline mặc định | mỗi con số so sánh ghi rõ đối thủ là ai và đã tune hay chưa |
| L10 | Một phát biểu sai về thông tin Fisher tồn tại qua nhiều bản vì không ai rà lại phần cũ | mỗi vòng rà toán rà cả phần kế thừa, không chỉ phần mới |
| L11 | Trung bình đẹp che trung vị gần 0; lợi ích dồn vào một nhóm dataset | luôn báo cáo trung vị, số thắng/hoà/thua và phân rã theo nhóm cạnh trung bình |
| L12 | Thiết kế một bối cảnh "khó" theo trực giác, hoá ra dễ | trước khi thiết kế bối cảnh, viết dự đoán có lý do; nếu có lý thuyết thì tính trước |

## 4. Quy tắc riêng cho thước đo tỉ giá

1. **Luôn báo cáo hai thước đo cạnh nhau:** tỉ giá quy đổi (chính) và phần khoảng cách naive → oracle đã lấy lại (phụ). Hai thước đo có thể kể hai câu chuyện khác nhau trên cùng một dataset.
2. **Đường học của oracle** phải có lưới đủ dày ở vùng dốc và được chạy với cùng TFM, cùng tiền xử lý, cùng giới hạn ngữ cảnh như phương pháp.
3. **n_eff ngoài khoảng đã chạy thì ghi cận**, không ngoại suy.
4. **Khoảng tin cậy của tỉ giá** lấy bằng bootstrap theo seed và theo dataset; tổng hợp trên thang log.
5. **Chỉ số định nghĩa n_eff được chọn trước** (một chỉ số chính cho mỗi loại nhãn yếu).
6. **Tỉ giá trần luôn kèm tên mô hình tham chiếu** mà nó được suy ra; không gọi là "giới hạn của TFM".

## 5. Dataset là tài nguyên tiêu hao

- Mỗi dataset dùng cho một nghiên cứu xác nhận là "cháy": chỉ còn dùng được làm tập phát triển. Ghi ngay vào `v3/datasets/USED_DATASETS.csv`.
- Trước khi thiết kế một nghiên cứu xác nhận, đếm xem còn bao nhiêu dataset mới thoả tiêu chí. Bài v2 đã dùng gần hết ứng viên trong 9 suite OpenML thông dụng.
- Tiêu chí chọn và danh sách loại trừ (trùng nguồn, nằm trong tập huấn luyện của TFM) được viết trước khi xem dữ liệu.

## 6. Ba phòng phản biện độc lập

Mỗi bản nháp gửi thầy đi qua ba phòng, mỗi phòng là một agent chưa tham gia viết, không thấy biên bản của phòng khác:

| Phòng | Việc | Sản phẩm |
|---|---|---|
| Toán | rà từng định nghĩa, giả định, bước chứng minh; tìm phản ví dụ; rà cả phần kế thừa | biên bản có mức Nghiêm trọng / Lớn / Nhỏ |
| Kiểm toán số liệu | tái tạo mọi con số trong bài từ dữ liệu thô bằng code riêng | bảng số trong bài so với số tái tạo |
| Kiểu NeurIPS | chấm theo bốn mặt ở mục 1, cho điểm, nêu ba lý do từ chối mạnh nhất | biên bản và điểm |

Sau mỗi vòng: lập bảng "ý phản biện → cách xử lý", kể cả các ý **không** xử lý và lý do. Vòng kế tiếp kiểm việc sửa.

## 7. Hai bài từ một dòng nghiên cứu

Bài v2 và bài v3 có chung phương pháp và code. Quy tắc 11 (không chia nhỏ một kết quả, không tự đạo văn, không nộp song song) được cụ thể hoá ở `v3/OVERLAP_WITH_V2.md`. Rà lại tài liệu đó ở G9 và G11.

## 8. Khi một mốc không đạt

- Điều kiện dừng của từng mốc được viết trong `v3/V3_PLAN.md` trước khi mốc bắt đầu.
- Khi một điều kiện dừng bị chạm: ghi kết quả vào `FINDINGS.md`, thu hẹp hoặc đổi tuyên bố trong ma trận khẳng định, rồi mới bàn hướng tiếp. Không chạy thêm thí nghiệm để "cứu" tuyên bố cũ.
