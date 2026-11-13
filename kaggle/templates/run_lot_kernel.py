"""run_lot_kernel.py — script chạy MỘT lượt v3 trên Kaggle, dùng cho chế độ đẩy bằng Kaggle CLI (kaggle kernels push).

Làm đúng những gì hai ô notebook thủ công làm (docs/claude-science/03_QUY_TRINH_KAGGLE.md):
  1. cài đúng phiên bản gói; 2. lấy TABPFN_TOKEN từ Kaggle Secrets nếu notebook có gắn (không bắt buộc với TabICL);
  3. chép code từ dataset đầu vào (gói v3_code_vN) vào /kaggle/working/code; 4. chép output cũ (nếu gắn làm đầu vào)
  để chạy tiếp; 5. chạy run_v3_lot.sh với giới hạn 11 giờ.
Sửa hai hằng số LOT và BUNDLE trước khi đẩy. KHÔNG ghi token hay khoá nào vào file này.
"""
import glob
import os
import shutil
import signal
import subprocess
import sys

LOT = "SMOKE"          # tên lượt trong run_v3_lot.sh
BUNDLE = "v3_code_v1"  # tên gói code trong dataset đầu vào
PIP = ["tabicl==2.2.0", "tabpfn==9.2.0", "tabdpt==1.3.1", "cleanlab==2.9.0", "dill"]

subprocess.run([sys.executable, "-m", "pip", "install", "-q", *PIP], check=True)
try:
    from kaggle_secrets import UserSecretsClient
    os.environ["TABPFN_TOKEN"] = UserSecretsClient().get_secret("TABPFN_TOKEN")
except Exception:
    pass
src = glob.glob(f"/kaggle/input/**/{BUNDLE}/code/run_v3_lot.sh", recursive=True)
print(src)
assert len(src) == 1, "không thấy đúng một gói code trong dữ liệu đầu vào"
shutil.rmtree("/kaggle/working/code", ignore_errors=True)
shutil.copytree(os.path.dirname(src[0]), "/kaggle/working/code", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
for pat in ("v3_*.csv", "v3_npz/*.npz"):                       # output phiên trước, nếu được gắn làm đầu vào
    for f in glob.glob(f"/kaggle/input/**/{pat}", recursive=True):
        rel = "v3_npz" if "/v3_npz/" in f else ""
        os.makedirs(os.path.join("/kaggle/working", rel), exist_ok=True)
        shutil.copy(f, os.path.join("/kaggle/working", rel))
os.chdir("/kaggle/working/code")
log = f"/kaggle/working/v3_{LOT}_master_log.txt"
with open(log, "a") as fh:
    p = subprocess.Popen(["bash", "run_v3_lot.sh", LOT, "/kaggle/working"], stdout=fh, stderr=subprocess.STDOUT,
                         start_new_session=True)
    try:
        p.wait(timeout=11 * 3600)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGTERM)
        p.wait()
        print("Dừng sau 11 giờ để kịp lưu output; cần phiên tiếp theo.")
print(open(log).read()[-4000:])
