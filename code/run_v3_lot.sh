#!/usr/bin/env bash
# run_v3_lot.sh <LƯỢT> <THƯ_MỤC_KẾT_QUẢ> — các lượt Kaggle của bài v3 (kho neur-v3).
#
# Mỗi lượt: ghi pip freeze, GPU, mã băm code (v3_<LƯỢT>_code_sha256.txt, để tools/intake_results.py đối chiếu với gói);
# chạy pytest, hỏng thì dừng; rồi chạy phần việc của lượt. Lượt chạy tiếp được nếu phần việc của nó chạy tiếp được.
#
# Các lượt:
#   SMOKE  kiểm kỹ thuật ngữ cảnh nhãn mềm với trọng số TabICL v2 thật (smoke_softctx.py). Không đo chất lượng.
#          Cần: GPU (một T4 là đủ), Internet On (tải trọng số TabICL từ HuggingFace). Không cần secret. Vài phút.
#   A1     (chưa có: thêm sau khi v3/A1_PILOT_PLAN.md được đóng băng)
set -u
LOT=${1:?thiếu tên lượt}
OUT=${2:-/kaggle/working}
mkdir -p "$OUT"
echo "lượt $LOT bắt đầu: $(date)"
pip freeze > "$OUT/v3_${LOT}_pip_freeze.txt" 2>&1
nvidia-smi --query-gpu=index,name,memory.total --format=csv > "$OUT/v3_${LOT}_gpu.txt" 2>&1
sha256sum $(find . -name "*.py" -o -name "*.sh" | sort) > "$OUT/v3_${LOT}_code_sha256.txt"
TESTS=tests
[ "$LOT" = "SMOKE" ] && TESTS="tests/test_softctx.py"   # lượt kiểm nhanh: chỉ test của phần đang kiểm
if ! python -m pytest -q $TESTS > "$OUT/v3_${LOT}_pytest.log" 2>&1; then
  echo "TEST HỎNG — dừng lượt $LOT. Xem v3_${LOT}_pytest.log"; tail -5 "$OUT/v3_${LOT}_pytest.log"; exit 1
fi
tail -1 "$OUT/v3_${LOT}_pytest.log"

case "$LOT" in
  SMOKE)
    python smoke_softctx.py --out "$OUT" > "$OUT/v3_SMOKE.log" 2>&1
    echo "SMOKE xong (mã thoát $?): $(date)"
    ;;
  *)
    echo "không có lượt $LOT"; exit 1
    ;;
esac
echo "lượt $LOT xong: $(date)"
