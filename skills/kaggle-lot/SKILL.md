---
name: kaggle-lot
description: Chuẩn bị, chạy, theo dõi và nhận kết quả một lượt thí nghiệm của kho neur-v3 trên Kaggle (2 x T4) - đóng gói code, ô notebook cho thầy, hoặc đẩy bằng Kaggle CLI, rồi kiểm và nhận kết quả. Dùng mỗi khi một thí nghiệm cần GPU hay dữ liệu OpenML.
---

# Một lượt Kaggle của bài v3

Mọi thí nghiệm của bài v3 chạy trên Kaggle (GPU T4 × 2, Internet On). Máy của thầy (MacBook M1) chỉ dùng cho code, test CPU, phân tích và viết. Chi tiết: `docs/claude-science/03_QUY_TRINH_KAGGLE.md`.

## 1. Trước khi chạy (bắt buộc)

1. Kế hoạch của lượt đã đóng băng (skill `neur-v3-research`, mục 3), hoặc lượt là kiểm kỹ thuật như SMOKE.
2. Lượt có mục trong `code/run_v3_lot.sh`; chạy tiếp được nếu dài hơn một phiên.
3. `cd code && python -m pytest -q tests` qua hết.
4. Commit mọi thay đổi trong `code/`.
5. Đóng gói: `python -I tools/make_code_bundle.py <N>`, với N tăng dần, không dùng lại. Ghi `v3_code_vN` và commit vào `v3/EXPERIMENT_LOG.md`.

## 2a. Chế độ thủ công (mặc định; thầy bấm chạy)

Gửi thầy file `_bundles/v3_code_vN.zip` và đoạn hướng dẫn sau, đã điền LOT và N:

- Kaggle → Datasets → dataset `neur-v3-code` → New Version → tải lên zip (lần đầu: New Dataset, tên `neur-v3-code`, Private).
- Notebook mới: Accelerator **GPU T4 × 2**; Internet **On**; Add Input → dataset `neur-v3-code` (bản mới nhất). Chỉ thêm Secret `TABPFN_TOKEN` khi lượt dùng TabPFN. Chạy tiếp phiên trước: Add Input → Your Work → output của notebook phiên trước.
- **Ô 1** (cài đặt, chép code, chép output cũ) và **Ô 2** (chạy lượt với giới hạn 11 giờ): chép nguyên văn từ `docs/claude-science/03_QUY_TRINH_KAGGLE.md` mục 1.2, chỉ sửa `BUNDLE` và `LOT`.
- Khi xong: tab Output → tải mọi file (Download All) → đặt zip vào `_incoming/` của kho, hoặc gửi trong cuộc trò chuyện.

## 2b. Chế độ Kaggle CLI (tuỳ chọn; dùng khi thầy đã bật và đã thử một lần)

Khoá Kaggle nằm ở thư mục khoá ngoài kho (ví dụ `~/research/kaggle-cred/kaggle.json`), thư mục đó được cấp quyền chỉ đọc. Mọi lệnh đặt `KAGGLE_CONFIG_DIR` trỏ tới đó. Không in nội dung khoá ra màn hình.

```bash
export KAGGLE_CONFIG_DIR=~/research/kaggle-cred
python -I tools/make_code_bundle.py N --kaggle-user <TEN>
kaggle datasets version -p _bundles/v3_code_vN -m "v3_code_vN (commit <hash>)" --dir-mode zip
# lần đầu: kaggle datasets create -p _bundles/v3_code_vN --dir-mode zip
mkdir -p _kernels/<LOT> && cp kaggle/templates/* _kernels/<LOT>/   # sửa id, title, LOT, BUNDLE
kaggle kernels push -p _kernels/<LOT>
kaggle kernels status <TEN>/neur-v3-<lot>
kaggle kernels output <TEN>/neur-v3-<lot> -p _incoming/<LOT>_raw -o
```

- Hỏi thầy trước mỗi lần `push`, vì mỗi lần dùng hạn mức GPU của thầy (khoảng 30 giờ mỗi tuần).
- Kiểm trạng thái thưa (15–30 phút một lần), không dồn dập.
- Nếu `push` báo lỗi về machine shape hay quyền, dừng và chuyển sang chế độ thủ công.

## 3. Nhận kết quả

```bash
python -I tools/intake_results.py --lot <LOT> --bundle _bundles/v3_code_vN <các zip hay thư mục output>
```

- "mọi kiểm tra qua" thì chép CSV, log, txt, npz vào `v3/raw/<LOT>/`. Không chép `code/`, `PRODEN/`, hay file của bên thứ ba.
- Có vấn đề (lệch mã băm, test hỏng, Traceback) thì báo thầy và không chấm.
- Ghi nhật ký: thời gian chạy, số ô, kết quả kiểm.

## 4. Bài học từ bài v2 (đã xảy ra)

- Lượt dài bị dừng ở mốc 11 giờ: luôn thiết kế để chạy tiếp, và ước thời gian trước.
- Thiếu ô do dừng giữa chừng: kế hoạch phải có quy tắc chấm khi thiếu ô, viết trước.
- Đường dẫn tệp đầu vào trên Kaggle khác nhau giữa các phiên: luôn tìm bằng `glob` đệ quy và `assert` đúng một kết quả.
- Trọng số TFM tải từ HuggingFace cần Internet On.
