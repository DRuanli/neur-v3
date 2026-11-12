# neur-v3 — bài v3: tỉ giá quy đổi của nhãn yếu dưới mô hình nền tảng bảng đóng băng

Kho riêng tư của bài v3 (đích NeurIPS 2027). Tách khỏi bài v2 (*In-Context Gibbs*, kho `icgibbs`) theo quyết định ngày 12/11/2026.

**Bắt đầu từ [`HANDOFF.md`](HANDOFF.md).**

| Thư mục | Nội dung |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | quy tắc làm việc, nạp tự động ở mỗi phiên |
| [`HANDOFF.md`](HANDOFF.md) | trạng thái, việc kế tiếp, việc chờ thầy |
| [`v3/`](v3/) | hồ sơ bài v3: chương trình nghiên cứu, những gì đã biết, ghi chú lý thuyết, tài liệu, ma trận khẳng định, kế hoạch thí điểm, phân tích định hướng |
| [`code/`](code/) | thư viện `icgibbs`, bộ chạy theo ô, script lượt Kaggle, test. Bản sống, phát triển tiếp cho v3 |
| [`research-handbook/`](research-handbook/) | sổ tay nghiên cứu (13 cổng G0–G12, thiết kế thực nghiệm, mẫu biểu); chương 11 dành riêng cho v3 |
| [`prior/`](prior/) | bản chụp đóng băng của dự án bài v1/v2: hồ sơ, code, kết quả, dữ liệu thô theo ô, bài v2, các biên bản phản biện. Không sửa |

## Đọc theo thứ tự

1. [`v3/V3_PLAN.md`](v3/V3_PLAN.md): luận điểm, sáu tuyên bố, các mốc và điều kiện dừng, rủi ro.
2. [`v3/FINDINGS.md`](v3/FINDINGS.md): mọi phát hiện kế thừa, kèm nơi lấy số.
3. [`v3/THEORY_NOTES.md`](v3/THEORY_NOTES.md): tỉ giá trần (bản nháp, chưa rà độc lập).
4. [`v3/G2/LITERATURE.md`](v3/G2/LITERATURE.md): tài liệu đã có, đã thấy, phải tra.
5. [`v3/M2_PILOT_PLAN.md`](v3/M2_PILOT_PLAN.md): bản nháp thí điểm đầu tiên.
6. [`research-handbook/11_BAI_V3_CHUAN_8_10.md`](research-handbook/11_BAI_V3_CHUAN_8_10.md): chuẩn của một bài mức 8–10 và các bài học từ bốn vòng phản biện bài v2.

## Chạy kiểm thử (CPU)

```bash
cd code
pip install numpy scipy scikit-learn pandas torch pytest
python -m pytest -q tests
```

Mã truy cập TabPFN chỉ đặt qua biến môi trường `TABPFN_TOKEN` (Kaggle Secrets); không bao giờ ghi vào kho.
