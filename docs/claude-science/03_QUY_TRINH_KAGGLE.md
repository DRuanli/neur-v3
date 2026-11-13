# 03 · Quy trình chạy thực nghiệm trên Kaggle

Mọi thí nghiệm của bài v3 chạy trên Kaggle: notebook GPU **T4 × 2**, **Internet On**, mỗi phiên tối đa khoảng 12 giờ, hạn mức GPU khoảng 30 giờ mỗi tuần (Kaggle có thể đổi). Claude Science trên máy thầy chuẩn bị mọi thứ, rồi nhận, kiểm và chấm kết quả.

```
Claude Science (máy thầy)                 Kaggle                                Claude Science
─────────────────────────                 ──────                                ──────────────
kế hoạch + dự đoán + script chấm
 → commit đóng băng
code + test → commit
make_code_bundle.py → v3_code_vN.zip ──→ dataset "neur-v3-code" (phiên bản mới)
                                          notebook: Ô 1 (cài, chép code)
                                                    Ô 2 (run_v3_lot.sh LƯỢT)
                                          output: v3_<LƯỢT>_*.csv/log/npz ──→ _incoming/ (zip)
                                                                                intake_results.py (kiểm)
                                                                                → v3/raw/<LƯỢT>/
                                                                                → script chấm (một lần)
                                                                                → báo cáo, cập nhật hồ sơ
```

## 1. Chế độ thủ công (mặc định, đã dùng suốt bài v2)

### 1.1 Lần đầu: tạo dataset chứa code

1. Claude (hoặc thầy) chạy `python -I tools/make_code_bundle.py 1` → `_bundles/v3_code_v1.zip`.
2. kaggle.com → **Datasets** → **New Dataset** → tải lên `v3_code_v1.zip` → tên `neur-v3-code` → **Private** → Create.
3. Các lần sau: mở dataset `neur-v3-code` → **New Version** → tải lên `v3_code_vN.zip` mới.

### 1.2 Mỗi lượt: một notebook

1. **New Notebook**.
2. Settings: Accelerator **GPU T4 × 2**; Internet **On**.
3. **Add Input** → dataset `neur-v3-code` (bản mới nhất).
4. Chạy tiếp một lượt dang dở: **Add Input** → **Your Work** → output của notebook phiên trước.
5. Lượt nào dùng TabPFN: **Add-ons > Secrets** → bật `TABPFN_TOKEN`. TabICL không cần.
6. Dán hai ô dưới đây, sửa `BUNDLE` và `LOT`.
7. **Save Version → Save & Run All (Commit)** để chạy nền (nên dùng cho lượt dài), hoặc chạy trực tiếp khi lượt ngắn như SMOKE.

**Ô 1:**

```python
!pip install -q tabicl==2.2.0 tabpfn==9.2.0 tabdpt==1.3.1 cleanlab==2.9.0 dill
import os, glob, shutil
from kaggle_secrets import UserSecretsClient
try:
    os.environ["TABPFN_TOKEN"] = UserSecretsClient().get_secret("TABPFN_TOKEN")
except Exception:
    pass
BUNDLE = "v3_code_v1"                     # sửa theo gói mới nhất
src = glob.glob(f"/kaggle/input/**/{BUNDLE}/code/run_v3_lot.sh", recursive=True)
print(src); assert len(src) == 1
shutil.rmtree("/kaggle/working/code", ignore_errors=True)
shutil.copytree(os.path.dirname(src[0]), "/kaggle/working/code",
                ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
os.makedirs("/kaggle/working/v3_npz", exist_ok=True)          # chạy tiếp: chép output phiên trước
for f in glob.glob("/kaggle/input/**/v3_npz/*.npz", recursive=True):
    shutil.copy(f, "/kaggle/working/v3_npz/")
for f in glob.glob("/kaggle/input/**/v3_*.csv", recursive=True):
    shutil.copy(f, "/kaggle/working/")
print(len(glob.glob("/kaggle/working/v3_*.csv")), "csv cũ;", len(glob.glob("/kaggle/working/v3_npz/*.npz")), "npz cũ")
```

**Ô 2:**

```python
LOT = "SMOKE"                             # sửa theo lượt
import subprocess, os, signal
os.chdir("/kaggle/working/code")
log_path = f"/kaggle/working/v3_{LOT}_master_log.txt"
with open(log_path, "a") as log:
    p = subprocess.Popen(["bash", "run_v3_lot.sh", LOT, "/kaggle/working"], stdout=log,
                         stderr=subprocess.STDOUT, start_new_session=True)
    try:
        p.wait(timeout=11 * 3600)
        print("Lượt chạy xong.")
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGTERM); p.wait()
        print("Đã dừng sau 11 giờ để lưu output; cần phiên tiếp theo.")
print(open(log_path).read()[-4000:])
```

### 1.3 Khi xong

- Tab **Output** của notebook (hoặc của phiên bản đã commit) → **Download All**, được một zip.
- Đặt zip vào `~/research/neur-v3/_incoming/`, hoặc kéo vào cuộc trò chuyện trong Claude Science.
- Bảo Claude: "nhận kết quả lượt <LƯỢT>" (prompt P2 trong `PROMPTS_NGHIEN_CUU.md`).

## 2. Chế độ Kaggle CLI (tuỳ chọn, Claude tự đẩy và tự tải)

**Chưa thử từ môi trường của em.** Hãy thử một lần với lượt SMOKE trước khi dùng cho lượt thật.

1. Có khoá ở `~/research/kaggle-cred/` (`01_CAI_DAT_MAY_LOCAL.md` mục 4); cấp thư mục đó **Read-only** cho Project.
2. Duyệt các địa chỉ mạng `www.kaggle.com` và `storage.googleapis.com` khi được hỏi.
3. Claude dùng các lệnh trong skill `kaggle-lot` (mục 2b):
   - tải gói lên bằng `kaggle datasets version`;
   - đẩy notebook dạng script từ `kaggle/templates/` bằng `kaggle kernels push`, với `machine_shape: "NvidiaTeslaT4"` (GPU T4 × 2);
   - theo dõi bằng `kaggle kernels status`;
   - tải output bằng `kaggle kernels output`.
4. **Secret `TABPFN_TOKEN` không đặt được qua CLI.** Lượt cần TabPFN: thầy tạo notebook một lần trên web, gắn Secret, rồi Claude đẩy phiên bản mới vào đúng notebook đó (`id` trong `kernel-metadata.json`). Chưa kiểm được Secret có giữ nguyên qua các lần đẩy hay không; kiểm ở lần đầu. Lượt chỉ dùng TabICL không cần Secret.
5. Claude phải hỏi thầy trước mỗi lần `kaggle kernels push`, vì mỗi lần dùng hạn mức GPU của thầy.

## 3. Kiểm và nhận kết quả (cả hai chế độ)

```bash
python -I tools/intake_results.py --lot <LƯỢT> --bundle _bundles/v3_code_vN _incoming/<file>.zip
```

Công cụ này:
- giải nén vào thư mục mới `_incoming/<LƯỢT>_<thời điểm>/`, từ chối đường dẫn nguy hiểm;
- so mã băm code đã chạy với gói đã gửi;
- đọc kết quả pytest đầu lượt; đếm dòng và trạng thái của mọi CSV; tìm Traceback trong log;
- ghi `INTAKE_REPORT.json`.

Đã thử ngày 13/11/2026 trên hai gói S3B và S3BC: 87 file khớp mã băm, test 170 qua, 67 file npz, không có Traceback.

Chỉ khi "mọi kiểm tra qua" mới chép dữ liệu vào `v3/raw/<LƯỢT>/` và chấm.

## 4. Sự cố thường gặp

| Sự cố | Cách xử lý |
|---|---|
| Ô 1 báo `assert len(src) == 1` | chưa thêm dataset `neur-v3-code`, sai `BUNDLE`, hoặc gắn hai phiên bản; xem danh sách in ra |
| "TEST HỎNG — dừng lượt" | gửi `v3_<LƯỢT>_pytest.log` cho Claude; không chạy tiếp |
| Lượt dừng ở 11 giờ | phiên mới: thêm output phiên trước làm Input, dán y hệt hai ô |
| Không tải được trọng số TabICL | kiểm Internet On; thử lại sau |
| Hết hạn mức GPU tuần | chờ Kaggle đặt lại hạn mức; Colab miễn phí là phương án phụ (cần chuyển Ô 1 sang Google Drive) |
