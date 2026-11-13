# Mốc A1: thí điểm SCI-0 (ngữ cảnh nhãn mềm, TFM đóng băng)

- **Trạng thái: BẢN NHÁP ngày 13/11/2026, chưa đóng băng.** Hướng SCI đã chốt (`V3_PLAN.md` Q1–Q3). Đóng băng sau khi: code `sci_once`, `sci_mf` được gắn vào bộ chạy và qua test; lượt SMOKE xong; thầy duyệt Q4. Làm theo prompt P3 trong `docs/claude-science/PROMPTS_NGHIEN_CUU.md`. Khi đóng băng, ghi commit vào đây.
- **Loại:** thăm dò trên tập phát triển. Kết quả không là khẳng định của bài.

## 1. Câu hỏi

1. TabICL v2 đóng băng có dùng được nhãn mềm trong ngữ cảnh không, tức SCI-0 một lượt có hơn TFM ngây thơ (rút một ứng viên ngẫu nhiên) không?
2. Trường trung bình trong ngữ cảnh (`sci_mf`) đứng ở đâu so với một chuỗi Gibbs, với số lần gọi TFM ít hơn nhiều?
3. Lợi hay hại tập trung ở mức nhập nhằng nào?

## 2. Dữ liệu

- **PLL:** 24 dataset đa lớp của Study 1 và Study 2, đều có tối đa 10 lớp. Đều đã "cháy", nên là tập phát triển hợp lệ (`datasets/USED_DATASETS.csv`). Cùng lần chia, cùng seed 0, 1, 2 như hai study đó.
- **Mức q:** 0,3; 0,6; 0,8. Mức 0,8 mới, để có vùng nhập nhằng cao.
- **Nhãn nhiễu:** 10 dataset nhị phân của Study 1 ở các mức nhiễu của Study 1.
- **Giới hạn ngữ cảnh:** 2.000 điểm, như bài v2.

## 3. Phương pháp (một TFM: TabICL v2)

| Mã | Mô tả | Lần gọi TFM ước tính |
|---|---|---|
| `naive` | ngữ cảnh với một ứng viên rút ngẫu nhiên (PLL) hoặc nhãn quan sát (nhãn nhiễu) | 1 |
| `gibbs_warm` | một chuỗi In-Context Gibbs, cấu hình v1 (10 khối, 30 vòng) | khoảng 310 |
| `hard_em_warm` | hard-EM với TFM, cùng điểm khởi động | như bài v2 |
| `sci_once` | ngữ cảnh mềm q = chuẩn hoá(ℓ), một lượt | 1 |
| `sci_mf` | trường trung bình trong ngữ cảnh: 5 vòng, 10 phần, λ = 0,5, q⁰ = chuẩn hoá(ℓ) | 51 |
| `oracle` | ngữ cảnh với nhãn thật | 1 |

## 4. Chỉ số

Accuracy cho PLL, AUC cho nhãn nhiễu (nhị phân). Mỗi cặp (dataset, mức) lấy trung bình 3 seed. Hoà khi |chênh| < 0,001.

## 5. Dự đoán ghi trước (chốt ngưỡng lúc đóng băng)

| Mã | Dự đoán | Lý do |
|---|---|---|
| P-A1-1 | PLL ở q 0,6 và 0,8: `sci_once` > `naive` ở ít nhất 2/3 số cặp | nhãn mềm mang mọi ứng viên, còn naive chỉ một ứng viên ngẫu nhiên |
| P-A1-2 | PLL, mọi mức: trung bình (`sci_mf` − `gibbs_warm`) ≥ −0,02 | trường trung bình dùng cùng thông tin với khoảng 1/6 số lần gọi |
| P-A1-3 | PLL q 0,8: `sci_mf` ≥ `gibbs_warm` ở ít nhất một nửa số cặp | ở vùng nhập nhằng cao, chuỗi Gibbs dễ kẹt; trường trung bình không có nhiễu lấy mẫu |
| P-A1-4 | Nhãn nhiễu: `sci_once` ≥ `naive` ở ít nhất một nửa số dataset | yếu: TFM vốn đã ít bị nhiễu nhãn ảnh hưởng |
| P-A1-5 | Lần gọi TFM của `sci_mf` ≤ 1/5 của `gibbs_warm` | theo thiết kế |

**Quy tắc dùng kết quả (ghi trước):**
- SCI-0 chỉ vào bài như một biến thể không huấn luyện nếu P-A1-2 đúng.
- Nếu P-A1-1 sai thì kết luận "TFM đóng băng không dùng được nhãn mềm" là một phát hiện của bài, và là lý do trực tiếp cho SCI-FT.
- Kết quả A1 không dừng hướng SCI.

## 6. Chi phí

- Khoảng 24 × 3 × 3 = 216 ô PLL và 30 ô nhãn nhiễu.
- Với khoảng 150 giây mỗi ô trên một T4 (chủ yếu là chuỗi Gibbs), tổng khoảng 10 giờ GPU, tức một phiên Kaggle 2 × T4.

## 7. Code cần viết trước khi đóng băng

1. Trong `code/icgibbs/g7/methods.py`: phương pháp `sci_once`, `sci_mf`, dùng `weak_model(cell).lik()` làm ℓ và `softctx.SoftContextTabICL`. Áp đúng giới hạn ngữ cảnh 2.000 điểm (lấy mẫu con hàng của X và Q cùng lúc), cùng cấu hình TabICL như backend `tabicl_v2` của bài v2.
2. Trong `run_g7.py`: cho phép mức q 0,8 ở split phát triển; ghi số lần gọi TFM.
3. Lượt `A1` trong một script lượt mới; pytest ở đầu lượt; chạy tiếp được.
4. `v3/analysis/a1_report.py`: chấm P-A1-1 đến P-A1-5; thử trên dữ liệu giả.
5. Test cho cả bốn mục.
