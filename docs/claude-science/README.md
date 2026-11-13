# Làm bài v3 trong Claude Science

*13/11/2026.* Bộ tài liệu này dựng một Project mới trong Claude Science (ứng dụng trên máy thầy) cho kho `neur-v3`. Mọi thực nghiệm chạy trên Kaggle.

## Đọc và làm theo thứ tự

| # | Tài liệu | Ai làm | Thời gian |
|---|---|---|---|
| 1 | [01_CAI_DAT_MAY_LOCAL.md](01_CAI_DAT_MAY_LOCAL.md): cài Claude Science, clone kho, khoá Kaggle (tuỳ chọn) | thầy | 30–45 phút |
| 2 | [02_TAO_PROJECT.md](02_TAO_PROJECT.md): tạo Project, cấp thư mục, cài skill, tiêu chí reviewer | thầy | 15 phút |
| 3 | [PROMPT_KHOI_DAU.md](PROMPT_KHOI_DAU.md): phiên đầu tiên | thầy dán; Claude làm | 30–60 phút |
| 4 | [03_QUY_TRINH_KAGGLE.md](03_QUY_TRINH_KAGGLE.md): chạy lượt SMOKE trên Kaggle | thầy bấm chạy | 15–30 phút |
| 5 | [PROMPTS_NGHIEN_CUU.md](PROMPTS_NGHIEN_CUU.md): P2 nhận kết quả SMOKE, rồi P3, P4… theo các mốc | thầy dán; Claude làm | theo mốc |

## Các file dán vào Claude Science

| File | Dán vào đâu |
|---|---|
| [PROJECT_INSTRUCTIONS.md](PROJECT_INSTRUCTIONS.md) | Custom instructions của Project |
| [REVIEWER_CRITERIA.md](REVIEWER_CRITERIA.md) | Settings > Specialists > Reviewer |
| `skills/neur-v3-research/`, `skills/kaggle-lot/` (ở gốc kho) | Settings > Skills > Add skill > Upload a skill (dạng zip) |

Tạo lại zip cho hai skill sau khi chúng thay đổi (từ gốc kho):

```bash
mkdir -p _bundles/skills && cd skills && for s in neur-v3-research kaggle-lot; do rm -f ../_bundles/skills/$s.zip; zip -qr ../_bundles/skills/$s.zip $s; done
```

## Công cụ trong kho dùng cho quy trình này

| Công cụ | Việc |
|---|---|
| `tools/make_code_bundle.py` | đóng gói `code/` thành `_bundles/v3_code_vN(.zip)`, kèm mã băm và commit; từ chối khi còn thay đổi chưa commit |
| `tools/intake_results.py` | giải nén kết quả Kaggle an toàn, so mã băm code, đọc pytest, đếm CSV, tìm Traceback |
| `code/run_v3_lot.sh` | các lượt Kaggle của v3 (hiện có: SMOKE) |
| `code/smoke_softctx.py` | lượt SMOKE: kiểm kỹ thuật ngữ cảnh nhãn mềm với trọng số TabICL v2 thật |
| `kaggle/templates/` | `kernel-metadata.json`, `run_lot_kernel.py` cho chế độ Kaggle CLI (tuỳ chọn, chưa thử) |

## Điều đã kiểm và chưa kiểm

| Mục | Trạng thái |
|---|---|
| Các bước cài đặt và khái niệm của Claude Science | theo tài liệu chính thức đọc ngày 13/11/2026; em **không** chạy được Claude Science từ môi trường của em |
| `intake_results.py` | đã thử trên gói kết quả S3B và S3BC thật: 87 file khớp mã băm |
| `make_code_bundle.py`, `smoke_softctx.py`, test | đã chạy; bộ test 176 qua, 5 bỏ qua (CPU) |
| Lượt SMOKE trên Kaggle với trọng số thật | **chưa chạy** (việc đầu tiên) |
| Chế độ Kaggle CLI (push, status, output; Secret qua CLI) | **chưa thử**; giá trị `machine_shape: "NvidiaTeslaT4"` cho GPU T4 × 2 lấy theo trả lời của người bảo trì kaggle-cli trên GitHub |
