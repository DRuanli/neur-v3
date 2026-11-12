# `prior/`: bản chụp đóng băng của dự án bài v1/v2

- **Nguồn:** kho `DRuanli/icgibbs`, thư mục `de-tai-moi/`, commit `120c4d9` (12/11/2026).
- **Quy tắc: không sửa gì trong thư mục này.** Nó là hồ sơ để bài v3 trích, đối chiếu và phân tích lại. Mọi việc mới làm ở `v3/` và `code/`. Nếu bài v2 có cập nhật (ví dụ kết quả S3B), cập nhật ở kho `icgibbs` rồi chép sang đây bằng một commit ghi rõ commit nguồn.
- **Bắt đầu đọc từ:** `HANDOFF.md` (trạng thái của dự án cũ), rồi `../v3/FINDINGS.md` (bản tổng hợp cho v3).

## Có gì

| Đường dẫn | Nội dung |
|---|---|
| `G1_*`, `G2/` … `G9/` | hồ sơ theo cổng của bài v1: chọn đề tài, tính mới, kế hoạch, phương pháp và chứng minh, giao thức đóng băng, Study 1, viết bài, phản biện |
| `S2/`, `S3/` | Study 2 và Study 3: kế hoạch ghi trước, script chấm, kết quả, báo cáo |
| `V2/` | giai đoạn phát triển phương pháp v2 (V0, V1A–V1D), lý thuyết động học (W1), chọn TFM (W4), kế hoạch bài v2 |
| `G4/code/` | thư viện `icgibbs`, bộ chạy, test, đúng như lúc sinh ra các kết quả ở đây. **Bản đóng băng**; bản để phát triển tiếp là `../code/` |
| `paper/` | bài v2 bản nháp 3: nguồn LaTeX, script sinh số và bảng, `main.pdf` |
| `G9/reviews/` | bốn biên bản phản biện độc lập của bài v2 và biên bản cũ của bài v1 |
| `*/raw/` | kết quả thô theo ô (CSV, log, pip freeze, mã băm code) và dự đoán của từng chuỗi (npz) |
| `docs/` | khai báo dùng AI, tái hiện baseline, mã băm dataset, không gian tune |

## Không có gì (và lấy ở đâu)

- Các file `*_preds.jsonl` (dự đoán từng điểm của Study 1, Study 2 và các lượt thí điểm, khoảng 400 MB) **không** được chép. Chúng nằm trong kho `icgibbs` ở cùng đường dẫn. Các script cần chúng: `G8/analysis/g8_descriptive.py`, `g8_pll_collapse.py` và một phần `S2/analysis/`.
- Kết quả S3B / S3BC: chưa chạy.
- Thư mục `V3/` của dự án cũ: đã chuyển thành `../v3/`.

## Chạy lại một phân tích

Các script giữ nguyên đường dẫn tương đối của dự án cũ, nên chạy từ thư mục `prior/`:

```bash
cd prior
python -I S3/s3_report.py      # chấm Study 3 từ 213 file npz
python -I S3/s3_explore.py     # phân tích thăm dò trên Study 3
```
