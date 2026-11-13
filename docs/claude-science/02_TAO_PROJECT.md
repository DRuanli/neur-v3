# 02 · Tạo Project "neur-v3" trong Claude Science

## 1. Tạo Project

1. Trang chủ Claude Science → **New project**.
2. Tên: `neur-v3 · SCI (NeurIPS 2027)`.
3. **Custom instructions** của Project: dán **nguyên văn** nội dung `PROJECT_INSTRUCTIONS.md` (phần giữa hai đường kẻ). Claude đọc hướng dẫn này ở đầu mọi phiên trong Project.

## 2. Cấp quyền thư mục

Ở phiên đầu, gõ đường dẫn vào ô soạn tin, hoặc dùng `@`. Khi thẻ "Access … on your computer?" hiện ra:

| Thư mục | Quyền | Ghi chú |
|---|---|---|
| `~/research/neur-v3` | **Read & write** | kho chính |
| `~/research/kaggle-cred` | **Read-only** | chỉ khi dùng chế độ Kaggle CLI |

- Không cấp cả thư mục nhà hay `~/Downloads`.
- Kết quả Kaggle: đặt zip vào `~/research/neur-v3/_incoming/`, hoặc đính kèm trong cuộc trò chuyện.
- Quyền đã cấp giữ nguyên giữa các phiên của Project; xem và thu hồi ở **Settings > Permissions**.

## 3. Cài hai skill của đề tài

Hai skill nằm trong `skills/` của kho và trong gói em gửi (`neur-v3-research.zip`, `kaggle-lot.zip`).

1. **Settings > Skills > Add skill > Upload a skill**.
2. Tải lên `neur-v3-research.zip`, rồi `kaggle-lot.zip`.
3. Kiểm: gõ `/` trong ô soạn tin, thấy `neur-v3-research` và `kaggle-lot`.

**Không dùng "Import from GitHub" với kho neur-v3:** Claude Science giới hạn 100 MB cho mỗi lần tải kho khi nhập skill, mà kho khoảng 190 MB. Khi skill thay đổi trong kho, tải lại zip: em hay Claude trong Claude Science tạo bằng lệnh ở `README.md` của thư mục này.

## 4. Tiêu chí cho bộ phận phản biện

**Settings > Specialists > Reviewer** → thêm tiêu chí: dán nội dung `REVIEWER_CRITERIA.md`. Reviewer kiểm các khẳng định của Claude so với những gì đã thực sự chạy. Nó không chạy lại phân tích, nên vẫn cần ba phòng phản biện độc lập trước khi nộp bài.

## 5. Các thiết lập khác

| Thiết lập | Đề xuất | Lý do |
|---|---|---|
| Memory | Bật | nhớ thói quen làm việc; không bao giờ để nó lưu token |
| Delegation (menu của từng phiên) | Bật khi cần rà độc lập hay tra tài liệu song song | quy tắc 7: người rà phải chưa tham gia |
| Auto mode | **Tắt** lúc đầu. Sau vài phiên có thể cho phép "This project" với Python và shell | thầy thấy được từng lệnh trước khi chạy |
| Connectors | Literature Graph bật; connector sinh học tuỳ ý | tra tài liệu |

## 6. Phiên đầu tiên

Dán `PROMPT_KHOI_DAU.md` (phần trong khung). Claude sẽ:
- đọc hồ sơ, tạo môi trường, chạy test;
- đóng gói code cho lượt SMOKE;
- báo cáo trạng thái và việc cần thầy làm trên Kaggle.

Các phiên sau: chọn prompt phù hợp trong `PROMPTS_NGHIEN_CUU.md`.

## 7. Vì sao tách Project này khỏi Project "TabPFN" trên claude.ai

- Project "TabPFN" (claude.ai) chứa hồ sơ bài v1/v2 (kho `icgibbs`).
- Project mới trong Claude Science làm việc trực tiếp trên kho `neur-v3` ở máy thầy; không cần tải tài liệu lên vì Claude đọc thẳng thư mục được cấp.
- Hồ sơ bài v2 đã có bản chụp đầy đủ ở `neur-v3/prior/`.
