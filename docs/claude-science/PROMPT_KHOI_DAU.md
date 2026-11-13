# Prompt khởi đầu (phiên đầu tiên của Project neur-v3 trong Claude Science)

Dán nguyên khung dưới đây vào phiên đầu. Phiên này chỉ dựng môi trường, kiểm kho và chuẩn bị lượt SMOKE; chưa chạy thí nghiệm nào.

```text
Chào em. Đây là phiên đầu tiên của Project neur-v3 trong Claude Science. Kho nằm ở ~/research/neur-v3 — hãy xin quyền
Read & write cho thư mục đó. (Nếu thầy đã tạo ~/research/kaggle-cred thì xin thêm quyền Read-only cho thư mục ấy; nếu chưa
thì bỏ qua.)

Việc của phiên này, làm theo thứ tự, dùng skill neur-v3-research:

1. Đọc CLAUDE.md, HANDOFF.md (mục 000 và 00 trước), v3/V3_PLAN.md, v3/A1_PILOT_PLAN.md, v3/FINDINGS.md (mục 3.3–3.4),
   v3/V3_IDEA_CHECK_2026-11-13.md, docs/claude-science/03_QUY_TRINH_KAGGLE.md. Tóm tắt cho thầy trong 8–10 dòng: bài v3
   là gì, đang ở mốc nào, các mốc tiếp theo và điều kiện dừng của chúng.
2. Kiểm kho: `git status`, `git log --oneline -5`; báo nếu có thay đổi chưa commit hay kho cũ hơn remote.
3. Tạo (hoặc dùng lại) môi trường Python tên `neur-v3` gồm numpy, scipy, pandas, scikit-learn, pytorch bản CPU cho Apple
   Silicon, pytest, tabicl==2.2.0, kaggle. Báo phiên bản đã cài.
4. Chạy `cd code && python -m pytest -q tests/test_softctx.py` rồi cả bộ `python -m pytest -q tests` (khoảng 10–15 phút).
   Lần chạy gần nhất (13/11/2026, môi trường Linux của phiên trước): 176 qua, 5 bỏ qua (5 test bỏ qua vì thiếu kho GLWS,
   PRODEN và gói sarpu — bình thường trên máy). Báo đúng con số; nếu có test hỏng thì dừng và cho thầy xem lỗi, không tự
   sửa test.
5. Chạy lại một phép tính cũ để chắc dữ liệu nguyên vẹn: `python -I v3/analysis/v3_s3b_check.py` và so với
   v3/results/v3_s3b_check.txt (phải trùng từng ký tự).
6. Chuẩn bị lượt SMOKE (kiểm kỹ thuật ngữ cảnh nhãn mềm với trọng số TabICL v2 thật; không đo chất lượng):
   `python -I tools/make_code_bundle.py 1`, rồi viết cho thầy hướng dẫn từng bước theo docs/claude-science/03_QUY_TRINH_KAGGLE.md
   mục 1 (BUNDLE = "v3_code_v1", LOT = "SMOKE"; GPU T4 × 2; Internet On; không cần Secret). Ghi một dòng vào
   v3/EXPERIMENT_LOG.md.
7. Nếu có khoá Kaggle: thử `KAGGLE_CONFIG_DIR=~/research/kaggle-cred kaggle kernels list --mine --page-size 3` (không in khoá).
   Chỉ báo chạy được hay không; KHÔNG đẩy lượt nào lên Kaggle.
8. Cập nhật HANDOFF.md (mục trên cùng: "Phiên Claude Science đầu tiên"), commit với thông điệp tiếng Anh; hỏi thầy trước
   khi git push.

Cuối phiên, báo cáo: (a) trạng thái môi trường và test, (b) file zip cần tải lên Kaggle và đường dẫn của nó,
(c) các việc cần thầy quyết, trong đó có Q4 ở v3/V3_PLAN.md §8 (duyệt bản nháp A1).
```

**Sau khi SMOKE chạy xong trên Kaggle:** đặt zip output vào `_incoming/` rồi dùng prompt **P2** trong `PROMPTS_NGHIEN_CUU.md`.
