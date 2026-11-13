# Bài v3: chương trình nghiên cứu — bản 3, hướng phát triển thuật toán

*Ngày 13/11/2026.*

- **Quyết định của thầy (13/11/2026):** v3 theo hướng phát triển thuật toán.
- **Các bản trước:** bản 2 (luận điểm "tỉ giá quy đổi", 12/11) ở `archive/V3_PLAN_ban2_ti_gia.md`; lý do bỏ ở `V3_IDEA_CHECK_2026-11-13.md`.
- **Trạng thái: ĐÃ CHỐT** (thầy, 13/11/2026 13:39: "chốt"). Q1–Q3 ở mục 8 được duyệt theo đề xuất; Q4 (đóng băng A1) duyệt khi code của A1 xong.
- **Đã có:** lõi kỹ thuật `code/icgibbs/softctx.py` cùng 9 test trên CPU (mô hình khởi tạo ngẫu nhiên), lượt kiểm kỹ thuật SMOKE với trọng số thật (chưa chạy).
- **Chưa có:** kết quả nào với trọng số thật.
- **Môi trường làm việc từ 13/11/2026:** Claude Science trên máy thầy, Project `neur-v3`, theo `docs/claude-science/`. Mọi thí nghiệm chạy trên Kaggle.

## 1. Vì sao cần một thuật toán mới: điều dữ liệu của bài v2 nói

Mọi số dưới đây lấy từ Study 3 và S3B (20 dataset mới, 4 TFM; `FINDINGS.md` §3.4, `V3_IDEA_CHECK_2026-11-13.md` §5).

| # | Quan sát | Số | Hệ quả cho thuật toán |
|---|---|---|---|
| 1 | Suy luận lặp trong ngữ cảnh (Gibbs, hard-EM) hỏng **vì thuật toán**, không vì thiếu thông tin, khi nhãn yếu nhập nhằng | PLL q 0,6: chuỗi đơn lấy lại 36% khoảng cách naive → oracle, A1 61%, X 77%. Cùng nhãn yếu: TabICL v2 61%, TabPFN-3 2% | thuật toán tốt hơn còn nhiều chỗ để thắng ở PLL |
| 2 | Thêm vòng quét hiếm khi cứu được chuỗi kẹt | 100 vòng sửa 5/35 ô kẹt (xem tạm) | không sửa được bằng chạy lâu hơn; phải đổi cách suy luận |
| 3 | Phương pháp tốt nhất hiện có rất đắt | X: khoảng 3.700 lần gọi TFM, trung vị 37 phút mỗi ô | một thuật toán rẻ hơn 100 lần đã là đóng góp thực tế |
| 4 | Vẫn còn khoảng cách tới oracle | X kém oracle tốt nhất 0,135 ở PLL, 0,052 ở LLP | trần còn cao, nhất là PLL |
| 5 | Ở LLP túi 8, mọi phương pháp dừng ở cùng một mức | spread trung vị 0,031 | ở LLP, thuật toán mới khó thắng về chất lượng; nếu thắng thì về chi phí |

## 2. Thuật toán đề xuất: suy luận với ngữ cảnh nhãn mềm (SCI, tên tạm)

**Ý tưởng một câu:** đưa thẳng nhãn yếu vào ngữ cảnh của TFM dưới dạng một phân phối trên các lớp, thay vì rút ra một nhãn cứng rồi lặp như Gibbs.

**Cơ sở kỹ thuật (đã kiểm 13/11):**
- TabICL v2 mã hoá nhãn ngữ cảnh bằng `Linear(one_hot(y))` ở hai chỗ (nhúng cột và học trong ngữ cảnh).
- Thay one_hot(y_i) bằng vector q_i thì embedding là tổ hợp lồi của các embedding lớp; với q_i one-hot, mô hình giữ nguyên. Test trên mô hình khởi tạo ngẫu nhiên: dự đoán với q one-hot trùng dự đoán với nhãn cứng, lệch dưới 10⁻⁵.
- Gói `tabicl` (BSD-3) có sẵn bộ sinh dữ liệu tổng hợp đã dùng để huấn luyện trước, mã huấn luyện và mã fine-tune. Mô hình có 27,6 triệu tham số.

### 2.1 SCI-0: không huấn luyện, dùng TFM đóng băng

- **Một lượt:** q_i = chuẩn hoá(ℓ_i), với ℓ_i là hệ số hợp lý của nhãn yếu (PLL: chỉ báo tập ứng viên; nhãn nhiễu: hàng ma trận chuyển; bán giám sát: vector đều cho điểm không nhãn). Một lần gọi TFM cho dự đoán.
- **Trường trung bình trong ngữ cảnh:** lặp q_i ← (1 − λ)·chuẩn hoá(ℓ_i ⊙ f(x_i | ngữ cảnh mềm của các phần khác)) + λ·q_i, chia phần chéo như các khối của Gibbs. Tất định, không có nhiễu lấy mẫu, mọi ứng viên được mang song song. Khoảng 25–50 lần gọi TFM thay cho khoảng 310 của một chuỗi Gibbs.
- Rủi ro: TFM chưa bao giờ thấy nhãn trộn khi huấn luyện, nên có thể dùng chúng kém. SCI-0 rẻ để thử và là đường cơ sở cho SCI-FT.

### 2.2 SCI-FT: khấu hao suy luận nhãn yếu vào TFM (thuật toán chính)

- **Huấn luyện:** fine-tune TabICL v2 sao cho **một lượt truyền xuôi** với ngữ cảnh nhãn yếu dạng mềm trả về p(y* | x*, X, nhãn yếu).
- **Dữ liệu huấn luyện:** các bài toán sinh từ chính bộ sinh tổng hợp của TabICL. Nhãn yếu được làm hỏng theo một họ cơ chế: PLL đều và phụ thuộc mẫu, nhãn nhiễu có ma trận chuyển, bán giám sát, nhãn bù.
- **Hàm mất mát:** entropy chéo trên nhãn thật của các điểm truy vấn, có thể thêm cả các điểm ngữ cảnh (dự đoán chuyển nạp).
- **Khởi tạo:** từ checkpoint TabICL v2, nên với nhãn one-hot mô hình xuất phát đúng từ TabICL v2. Có thể đóng băng phần nhúng cột và hàng để rẻ hơn.
- **Vì sao có thể thắng Gibbs và X:**
  - không còn lưu vực hay trộn chậm, vì không có chuỗi;
  - được huấn luyện trực tiếp cho đại lượng mà Gibbs nhắm tới;
  - 1–8 lần gọi thay cho khoảng 3.700.
- **Mở rộng:**
  - LLP: cần kênh cho thông tin túi (tỉ lệ của túi kèm danh tính túi), hoặc giữ vòng ngoài với quy hoạch động chính xác trên số đếm;
  - trên 10 lớp: gộp q theo nhóm của cây phân lớp của TabICL.

### 2.3 Lý thuyết cần xây

| Mã | Phát biểu dự kiến | Độ khó |
|---|---|---|
| T1 | Nghiệm tối ưu tổng thể của mục tiêu SCI-FT là phân phối dự đoán hậu nghiệm dưới (prior tổng hợp × cơ chế nhãn yếu). Đây chính là đại lượng mà In-Context Gibbs của bài v2 tính (Định lý 1 của v2). Vậy SCI-FT là In-Context Gibbs được khấu hao | thấp; mở rộng lập luận chuẩn của PFN |
| T2 | Khi cơ chế nhãn yếu lúc dùng khác lúc huấn luyện, sai số bị chặn bởi khoảng cách giữa hai cơ chế (theo bất đẳng thức xử lý dữ liệu) | trung bình |
| T3 | SCI-0: vì lớp đầu tuyến tính theo embedding nhãn, ngữ cảnh mềm là xấp xỉ bậc nhất (trường trung bình) của trung bình Gibbs; sai số chặn bởi độ cong của TFM theo embedding nhãn. Đo được độ cong này trên dữ liệu thật | trung bình–cao |

## 3. Các tuyên bố cần có (thay C1–C6 của bản 2)

| Mã | Tuyên bố | Bằng chứng cần |
|---|---|---|
| D1 | SCI-FT một lượt đạt ít nhất bằng X ở PLL, với dưới 1% số lần gọi TFM | Study 4 |
| D2 | SCI-FT hơn các baseline tốt nhất (nơ-ron đã tune, cây, kNN) ở PLL, nhãn nhiễu, bán giám sát, nhãn bù, và trên 3 bộ PLL thật | Study 4 |
| D3 | SCI không phụ thuộc điểm xuất phát; không cần nhiều điểm xuất phát | thí điểm A1–A2, Study 4 |
| D4 | T1 và T2 có chứng minh đã rà độc lập; T3 nếu được | M4 |
| D5 | LLP: SCI đạt mức của X với chi phí thấp hơn nhiều, hoặc kết quả âm được báo thẳng | A3 |
| D6 | Kết quả đứng trên dataset mới, ghi trước | Study 4 |

## 4. Các mốc và điều kiện dừng

| Mốc | Việc | Chi phí | Dừng hoặc đổi hướng nếu |
|---|---|---|---|
| **A0** | Lõi nhãn mềm và test (**xong 13/11**). Lượt SMOKE trên Kaggle: kiểm kỹ thuật với trọng số thật. Còn lại: gắn `sci_once`, `sci_mf` vào bộ chạy; tra tài liệu theo giao thức (prompt P4); ghi trước A1 (prompt P3) | CPU và 1 lượt SMOKE ngắn, 3–5 ngày | SMOKE cho thấy nhãn mềm one-hot không trùng nhãn cứng với trọng số thật (lệch ≥ 10⁻³) mà không sửa được; hoặc tìm thấy công trình đã làm đúng SCI-FT |
| **A1** | Thí điểm SCI-0 trên tập phát triển, chỉ suy luận (`A1_PILOT_PLAN.md`) | 1 phiên Kaggle | không dừng hướng; chỉ quyết định SCI-0 có vào bài hay không |
| **A2** | Thí điểm SCI-FT: fine-tune ngắn, ngữ cảnh ≤ 1.024 điểm, ≤ 10 lớp | khoảng 20–30 giờ T4 (3–4 phiên) | SCI-FT một lượt kém chuỗi Gibbs đơn ở PLL q 0,6 trên tập phát triển; hoặc mất mát trên tập kiểm tra tổng hợp không giảm so với lúc chưa fine-tune |
| **A3** | LLP, trên 10 lớp, nhãn bù; ablation (thành phần cơ chế huấn luyện, phần đóng băng, kích thước ngữ cảnh) | 2–4 phiên | — |
| **M4** | Lý thuyết T1–T3; rà độc lập | CPU | — |
| **A4** | Đếm dataset cho Study 4 với nguồn rộng hơn; tiêu chí ghi trước | CPU, từ 12/2026 | không đủ 20 dataset mới đạt tiêu chí |
| **Study 4** | Xác nhận ghi trước trên dataset mới: SCI-FT so với X, Gibbs, baseline tốt nhất từng loại; thêm PLL thật | 4–6 phiên | — |
| **M6** | Viết bài; ba phòng phản biện | — | — |

## 5. Rủi ro

| # | Rủi ro | Mức | Cách giảm |
|---|---|---|---|
| 1 | **Tài nguyên cho SCI-FT.** ICMIL (huấn luyện từ đầu) mất 12–24 giờ A100; T4 chậm hơn khoảng 5 lần | cao | fine-tune từ checkpoint thay vì huấn luyện từ đầu; đóng băng một phần; ngữ cảnh ngắn; Kaggle cùng Colab |
| 2 | **Cuộc đua tính mới.** In-Context PU (05/2026) và In-Context MIL (06/2026) cho thấy xu hướng: mỗi loại nhãn yếu một mô hình | cao | làm nhanh; điểm khác biệt là một mô hình cho nhiều loại nhãn yếu, khởi từ TFM có sẵn, nối với lý thuyết của Gibbs |
| 3 | Khoảng cách giữa cơ chế nhãn yếu tổng hợp và thật (PLL thật phụ thuộc mẫu) | trung bình | huấn luyện trên một họ cơ chế; đánh giá trên PLL thật; T2 |
| 4 | Chỉ làm trên TabICL v2: reviewer sẽ hỏi tính tổng quát | trung bình | kiểm encoder nhãn của TabDPT và TabPFN; nếu tuyến tính theo one-hot thì SCI-0 áp dụng được ngay |
| 5 | SCI-0 hỏng vì nhãn trộn nằm ngoài phân phối huấn luyện | trung bình | không ảnh hưởng hướng; SCI-FT xử lý đúng chỗ này |
| 6 | LLP không có lợi về chất lượng (quan sát 5 của mục 1) | trung bình | nhắm chi phí; báo kết quả âm nếu có |
| 7 | Trùng với bài v2 | thấp | Gibbs là baseline và là "đáp án đúng" để khấu hao; trích v2 |

## 6. Ranh giới với bài v2

- Bài v2: In-Context Gibbs, tức suy luận lặp với TFM đóng băng.
- Bài v3: SCI, tức đưa nhãn yếu vào chính đầu vào của TFM, có hoặc không huấn luyện.
- Gibbs xuất hiện trong v3 như baseline và như đại lượng mục tiêu của T1, có trích dẫn.
- Chi tiết: `OVERLAP_WITH_V2.md`.

## 7. Ước lượng của em

- Nếu A2 thành công (SCI-FT một lượt hơn rõ chuỗi Gibbs ở PLL): mức 6 trở lên khoảng 50–60%, mức 8 trở lên khoảng 20–25%.
- Xác suất A2 thành công, theo em, khoảng 40–50%.
- Gộp lại: mức 6 trở lên khoảng 35–45%, mức 8 trở lên khoảng 10–15%. Cao hơn hướng tỉ giá, vì điểm trần của một thuật toán thống nhất, rẻ và mạnh cao hơn một bài đo.

## 8. Việc cần thầy quyết

| # | Câu hỏi | Đề xuất của em |
|---|---|---|
| Q1 | Duyệt SCI (SCI-0 và SCI-FT) làm thuật toán của v3? | **đã duyệt 13/11** |
| Q2 | Ngân sách GPU: dùng hạn mức Kaggle khoảng 3–4 tuần cho SCI-FT, thêm Colab nếu cần? | **đã duyệt 13/11** |
| Q3 | Phạm vi: bắt đầu với nhãn yếu cấp mẫu (PLL, nhãn nhiễu, bán giám sát, nhãn bù), LLP ở mốc A3? | **đã duyệt 13/11** |
| Q4 | Duyệt bản nháp `A1_PILOT_PLAN.md` để em gắn code và đóng băng | chờ: duyệt khi code A1 xong (prompt P3) |

## 9. Các hướng thuật toán khác đã cân nhắc

| Hướng | Lý do không chọn làm chính |
|---|---|
| Gibbs có ủ nhiệt (làm mềm dự đoán của TFM rồi tăng dần) | sát với EM ủ tất định kinh điển; có thể dùng làm ablation |
| Trao đổi trạng thái giữa các chuỗi của nhiều TFM | phụ thuộc TFM tốt; thử nghiệm trộn TFM ở bài v2 cần 35–85% trọng số của TFM tốt |
| Ngữ cảnh chọn lọc theo độ tin cậy, mở dần | gần với các phương pháp tự huấn luyện theo lộ trình đã có |
| Huấn luyện từ đầu một TFM cho nhãn yếu | vượt tài nguyên; SCI-FT đạt cùng mục tiêu bằng fine-tune |
