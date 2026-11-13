# Prompt nghiên cứu cho Project neur-v3 (Claude Science)

Mỗi prompt là một phiên làm việc, xếp theo đúng thứ tự các mốc của `v3/V3_PLAN.md` (bản 3). Dán phần trong khung, sửa chỗ có `<...>`. Mọi prompt giả định Claude đã có Custom instructions của Project và hai skill `neur-v3-research`, `kaggle-lot`.

| Mã | Khi nào dùng |
|---|---|
| P0 | mở một phiên bất kỳ |
| P1 | chuẩn bị một lượt Kaggle |
| P2 | nhận và chấm kết quả một lượt |
| P3 | hoàn tất A0 và đóng băng thí điểm A1 |
| P4 | tra tài liệu theo giao thức |
| P5 | xây SCI-FT, chuẩn bị A2 |
| P6 | lý thuyết T1–T3 và rà độc lập |
| P7 | đếm dataset cho Study 4 |
| P8 | ghi trước Study 4 |
| P9 | viết bài và ba phòng phản biện |
| P10 | đóng phiên |
| P11 | việc của bài v2 (S3B B3) |

---

## P0 · Mở phiên

```text
Mở phiên. Đọc CLAUDE.md và mục trên cùng của HANDOFF.md, rồi báo trong 5 dòng: mốc hiện tại, việc kế tiếp, việc đang chờ
thầy, và có lượt Kaggle nào đang chạy hay kết quả nào trong _incoming/ chưa nhận. Chưa làm gì khác.
```

## P1 · Chuẩn bị một lượt Kaggle

```text
Chuẩn bị lượt <TÊN_LƯỢT> theo skill kaggle-lot.
- Kiểm kế hoạch của lượt đã đóng băng (ghi hash commit) — nếu lượt là thí nghiệm. SMOKE là kiểm kỹ thuật, không cần.
- Kiểm run_v3_lot.sh có mục cho lượt; ước thời gian chạy và số phiên.
- Chạy toàn bộ pytest; commit; đóng gói bằng tools/make_code_bundle.py với số phiên bản tiếp theo.
- Viết cho thầy hướng dẫn từng bước (chế độ thủ công, 03_QUY_TRINH_KAGGLE.md mục 1) đã điền BUNDLE và LOT, kèm thời gian
  ước tính và việc cần gắn (Secret, output phiên trước).
- <Tuỳ chọn, chỉ khi thầy cho phép:> dùng chế độ Kaggle CLI để tải gói và đẩy lượt; hỏi thầy trước lệnh push.
- Ghi nhật ký; cập nhật HANDOFF.
```

## P2 · Nhận và chấm kết quả

```text
Kết quả lượt <TÊN_LƯỢT> ở _incoming/<file>.zip (gói code đã gửi: _bundles/v3_code_v<N>).
1. Chạy tools/intake_results.py; nếu có vấn đề thì dừng, báo thầy, không chấm.
2. Nếu qua: chép CSV/log/txt/npz (không chép code/, PRODEN/) vào v3/raw/<TÊN_LƯỢT>/; kiểm đủ số ô so với kế hoạch.
3. Nếu là lượt có kế hoạch đóng băng: chạy script chấm ĐÚNG MỘT LẦN, không sửa; ghi thời điểm vào nhật ký. Nếu thiếu ô thì
   làm theo quy tắc thiếu ô của kế hoạch; mọi lần xem tạm đều ghi nhật ký.
   Nếu là SMOKE: đọc v3_SMOKE_report.json, báo K1–K4 (sai lệch one-hot/cứng, thời gian theo cỡ ngữ cảnh, bộ nhớ GPU).
4. Viết v3/<MỐC>_REPORT.md: dự đoán nào đúng, sai (giữ nguyên câu chữ dự đoán), số chính kèm trung vị, thắng/hoà/thua,
   khoảng tin cậy; mục "điều này có nghĩa gì cho kế hoạch" tách riêng và ghi là diễn giải.
5. Cập nhật FINDINGS.md, CLAIM_EVIDENCE_MATRIX.md, EXPERIMENT_LOG.md, HANDOFF.md; commit; báo thầy kết quả trước, việc cần
   quyết sau.
```

## P3 · Hoàn tất A0 và đóng băng A1

```text
Mốc A0, phần còn lại (v3/V3_PLAN.md §4; v3/A1_PILOT_PLAN.md §7). Thầy đã duyệt bản nháp A1.
1. Gắn hai phương pháp sci_once và sci_mf vào code/icgibbs/g7/methods.py (ℓ = weak_model(cell).lik(); predictor
   softctx.SoftContextTabICL cùng cấu hình TabICL v2 như backend tabicl_v2 của bài v2; giới hạn ngữ cảnh 2.000 điểm áp
   lên X và Q cùng lúc; ghi số lần gọi TFM). Thêm mức PLL q = 0,8 cho các split phát triển trong run_g7.py.
2. Thêm lượt A1 vào code/run_v3_lot.sh (hai GPU chia đều; chạy tiếp được).
3. Viết v3/analysis/a1_report.py chấm P-A1-1…P-A1-5; thử trên dữ liệu giả cùng định dạng.
4. Test cho mọi phần mới; chạy toàn bộ pytest.
5. Chốt các ngưỡng còn để mở trong A1_PILOT_PLAN.md (không đổi hướng dự đoán), đổi trạng thái thành ĐÓNG BĂNG, commit, ghi
   hash vào tài liệu, commit lần nữa.
6. Nhờ một nhánh độc lập (Delegation) rà A1_PILOT_PLAN.md và a1_report.py tìm chỗ mơ hồ trước khi đóng băng; sửa trước
   commit đóng băng.
7. Sau đó dùng P1 để chuẩn bị lượt A1.
```

## P4 · Tra tài liệu theo giao thức (cổng G2)

```text
Tra tài liệu cho SCI theo research-handbook/04_TONG_QUAN_TAI_LIEU.md, ghi vào v3/G2/NOVELTY_SEARCH_LOG.md (mẫu ở
research-handbook/templates/NOVELTY_SEARCH_LOG.md). Câu hỏi:
(a) đã có ai đưa nhãn mềm hay nhãn yếu vào ngữ cảnh của một TFM bảng (TabPFN, TabICL, TabDPT…) chưa — có hay không fine-tune;
(b) đã có mô hình kiểu PFN nào cho nhiều loại nhãn yếu cùng lúc chưa (ngoài In-Context PU 2605.05591, In-Context MIL
    2606.06458);
(c) suy luận "trường trung bình trong ngữ cảnh" hay khấu hao EM/Gibbs bằng transformer cho nhãn yếu;
(d) cập nhật mọi bài từ 06/2026 về TFM với nhãn nhiễu, bán giám sát, PLL, LLP.
Dùng connector Literature Graph (OpenAlex, arXiv) và web. Với mỗi bài liên quan: mở trang, ghi tên, tác giả, năm, nơi đăng
đúng như trang ghi, và nó phủ phần nào của D1–D6. Có thể dùng Delegation để chia (a)–(d). Kết luận: tính mới còn lại là gì,
có cần đổi kế hoạch không. Thêm các bài đã đối chiếu vào v3/G9/REFERENCE_CHECK.md (tạo mới nếu chưa có).
```

## P5 · Xây SCI-FT và chuẩn bị A2

```text
Mốc A2 (SCI-FT). Chỉ chuẩn bị, chưa chạy Kaggle.
1. Đọc mã tabicl.prior, tabicl.train và tabicl._finetune (gói tabicl==2.2.0 trong môi trường neur-v3) để hiểu cách sinh bài
   toán tổng hợp và vòng huấn luyện.
2. Viết code/icgibbs/sci_ft/ gồm: (a) bộ làm hỏng nhãn yếu cho một bài toán tổng hợp — PLL đều với q ∈ [0; 0,9], PLL phụ
   thuộc mẫu, nhãn nhiễu với ma trận chuyển, bán giám sát, nhãn bù; trả về ma trận ℓ; (b) vòng fine-tune: đầu vào ngữ cảnh
   là ℓ chuẩn hoá qua softctx, mất mát entropy chéo trên nhãn thật của điểm truy vấn, tuỳ chọn đóng băng phần nhúng
   cột/hàng, lưu checkpoint định kỳ để chạy tiếp qua nhiều phiên Kaggle; (c) đánh giá trên một tập bài toán tổng hợp giữ
   riêng.
3. Test trên CPU với checkpoint TabICL nhỏ khởi tạo ngẫu nhiên: mất mát giảm trong vài chục bước, checkpoint lưu và nạp lại
   cho cùng kết quả, ℓ one-hot thì mô hình trước fine-tune trùng TabICL gốc.
4. Viết v3/A2_PILOT_PLAN.md: ngân sách (≤ 30 giờ T4), cấu hình, điều kiện dừng từ V3_PLAN §4 (SCI-FT một lượt kém chuỗi
   Gibbs đơn ở PLL q 0,6 trên tập phát triển; hoặc mất mát giữ riêng không giảm), dự đoán có ngưỡng, script chấm.
   Chỉ dùng dataset phát triển. Nhờ một nhánh độc lập rà trước khi đóng băng.
5. Báo thầy ngân sách và lịch dùng GPU đề xuất.
```

## P6 · Lý thuyết T1–T3 và rà độc lập

```text
Viết v3/THEORY_SCI.md cho T1 (nghiệm tối ưu của mục tiêu SCI-FT là phân phối dự đoán hậu nghiệm dưới prior tổng hợp × cơ
chế nhãn yếu, tức đại lượng In-Context Gibbs của bài v2 nhắm tới — trích prior/paper/sections/appendix_proofs.tex),
T2 (chặn sai số khi cơ chế nhãn yếu lúc dùng khác lúc huấn luyện) và, nếu được, T3 (ngữ cảnh mềm là xấp xỉ bậc nhất của
trung bình Gibbs; sai số theo độ cong). Mỗi phát biểu: giả định đầy đủ, chứng minh, một kiểm số bằng mô phỏng trong
v3/analysis/, và một con số kiểm được trên dữ liệu thật (sổ tay chương 11, điều kiện 4).
Sau đó mở một nhánh Delegation CHƯA đọc chứng minh để rà như phòng phản biện toán (định nghĩa, giả định, từng bước, phản ví
dụ). Ghi biên bản vào v3/G9/reviews/, lập bảng ý phản biện → cách xử lý. Không dùng T1–T3 để viết dự đoán trước khi rà xong.
```

## P7 · Đếm dataset cho Study 4

```text
Mốc A4. Viết v3/STUDY4_DATASETS.md với tiêu chí chọn dataset ghi trước (số lớp, cỡ, loại feature, giấy phép, loại trùng
nguồn) và danh sách loại trừ (v3/datasets/USED_DATASETS.csv; tập huấn luyện đã công bố của từng TFM dùng trong Study 4,
ví dụ prior/V2/data/tabdpt_pretrain_ids.csv; các bộ cùng nguồn). Viết script đếm chạy trên Kaggle (môi trường này không gọi
được OpenML nếu mạng chặn — thử trước; nếu chặn thì chuẩn bị như một lượt Kaggle). Mục tiêu ít nhất 20 dataset mới cho PLL
và nhãn yếu cấp mẫu, cộng dữ liệu nhãn yếu thật (3 bộ PLL thật đã có ở bài v1; tìm thêm). Báo số đếm theo từng bước lọc.
```

## P8 · Ghi trước Study 4

```text
Viết v3/STUDY4_PLAN.md theo research-handbook/templates/EXPERIMENT_PROTOCOL.md và PREDICTIONS.md: giả thuyết H1–Hk ứng với
D1–D6, phép kiểm (Wilcoxon theo dataset, Holm), quy tắc hoà, quy tắc thiếu ô, baseline (X và In-Context Gibbs của bài v2;
nơ-ron đã tune; GBDT; kNN; các phương pháp mới nhất từ P4), ngân sách tune bằng nhau, dataset từ P7, seed, chi phí.
Viết v3/analysis/study4_report.py, thử trên dữ liệu giả. Nhờ hai nhánh độc lập rà (một nhánh như phản biện NeurIPS, một
nhánh như kiểm toán số liệu). Sửa, rồi chờ thầy duyệt trước khi đóng băng.
```

## P9 · Viết bài và ba phòng phản biện

```text
Viết bản nháp bài v3 (tiếng Anh, ẩn danh, mẫu NeurIPS 2027 nếu đã công bố) trong paper/ theo research-handbook/09 và
chương 11. Mọi số sinh bằng script thành macro (theo cách của prior/paper/scripts/make_v2.py). Không chép đoạn nào từ bài v2;
trích v2 theo v3/OVERLAP_WITH_V2.md. Sau mỗi bản nháp: ba nhánh Delegation độc lập — (1) phản biện toán, (2) kiểm toán số
liệu tái tạo mọi con số từ v3/raw/, (3) phản biện kiểu NeurIPS chấm Quality/Clarity/Significance/Originality và nêu ba lý
do từ chối mạnh nhất. Lập bảng ý phản biện → cách xử lý, kể cả ý không xử lý. Chạy checklist research-handbook/10 mục I.
```

## P10 · Đóng phiên

```text
Đóng phiên: cập nhật mục trên cùng của HANDOFF.md (đã làm gì, kết quả, việc kế tiếp, việc chờ thầy), EXPERIMENT_LOG.md,
CLAIM_EVIDENCE_MATRIX.md nếu có thay đổi; kiểm không có token hay khoá trong các file sắp commit; commit theo đợt nhỏ với
thông điệp tiếng Anh; hỏi thầy trước khi push. Báo cáo 5–8 dòng: kết quả trước, việc cần thầy quyết sau.
```

## P11 · Việc của bài v2: hoàn tất B3 của S3B (kho icgibbs, không phải kho này)

```text
Đây là việc của bài v2. Thầy đã clone kho icgibbs về ~/research/icgibbs; xin quyền Read & write cho thư mục đó. Kết quả
phiên 2 của lượt S3B ở <đường dẫn zip>. Kiểm như tools/intake_results.py (gói tham chiếu: mã của de-tai-moi/G4/code tại
commit b59ef14), chép vào de-tai-moi/S3/raw/S3B/, chạy `python -I S3/s3b_report.py` từ de-tai-moi (lần chấm B3 cuối), cập
nhật S3/S3B_REPORT.md mục 3–4 và V2/EXPERIMENT_LOG.md, commit. Sau đó chép báo cáo và dữ liệu mới sang
~/research/neur-v3/prior/S3/ bằng một commit ghi rõ commit nguồn.
```
