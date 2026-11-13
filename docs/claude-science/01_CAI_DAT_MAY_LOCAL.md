# 01 · Cài đặt trên máy của thầy (MacBook M1) để làm việc với Claude Science

*Viết ngày 13/11/2026 theo tài liệu chính thức của Claude Science lúc đó (claude.com/docs/claude-science). Claude Science đang ở giai đoạn beta, giao diện có thể đổi; khi một bước không khớp, làm theo tài liệu chính thức.*

## 0. Claude Science là gì, và vì sao hợp với bài v3

- Ứng dụng máy tính của Anthropic: Claude viết và chạy Python, R, shell trong một sandbox **trên máy thầy**, đọc và ghi đúng các thư mục thầy cấp quyền, lưu kết quả thành artifact có lịch sử phiên bản.
- Mỗi Project có hướng dẫn riêng mà Claude đọc ở đầu mọi phiên.
- Có skill tự viết, bộ phận phản biện (reviewer) kiểm khẳng định so với việc đã chạy, và Delegation để tách việc thành các nhánh song song.
- Máy M1 không có GPU NVIDIA, nên **mọi thí nghiệm vẫn chạy trên Kaggle**. Trên máy chỉ viết code, chạy test CPU, chấm, phân tích và viết bài. Quy trình Kaggle ở `03_QUY_TRINH_KAGGLE.md`.

## 1. Yêu cầu

| Mục | Yêu cầu |
|---|---|
| Tài khoản | Claude Pro, Max, Ultra, Team hoặc Enterprise (gói Free không dùng được). Team hay Enterprise: chủ tổ chức phải bật Claude Science |
| Máy | macOS 13 trở lên, Apple Silicon (M1) được hỗ trợ |
| Ổ đĩa | khoảng 5 GB cho Claude Science, thêm khoảng 0,5 GB cho kho `neur-v3` |
| Mạng | khu vực có claude.ai |
| Kaggle | tài khoản đã xác minh số điện thoại (để dùng GPU) |

## 2. Cài Claude Science

1. Vào claude.com/product/claude-science, tải bản **Mac (Apple Silicon)**.
2. Mở file, cài như ứng dụng thường.
3. Lần mở đầu, ứng dụng dựng môi trường chạy và hai môi trường Python, R khởi đầu (vài phút), rồi mở một tab trình duyệt. Không thấy tab: bấm biểu tượng **Claude Science** trên Dock.
4. **Đăng nhập** bằng tài khoản Claude (không cần API key). Nếu ứng dụng mở trong cửa sổ riêng: **Sign in on the web** rồi **Continue**.
5. **Trình hướng dẫn thiết lập:**
   - Connectors: bật Literature Graph (OpenAlex, arXiv). Nó cần một OpenAlex API key miễn phí, nhập ở **Settings > Credentials**. Có thể tắt các connector sinh học.
   - Skills: bật skill literature review.
   - Website: để mặc định; Claude sẽ hỏi từng trang khi cần.
   - Memory: bật.
6. Gặp lỗi về "Xcode license": mở Terminal, chạy `sudo xcodebuild -license accept`, rồi bảo Claude thử lại.

Dữ liệu của Claude Science nằm ở `~/.claude-science`. **Không sửa tay** bất cứ gì trong đó.

## 3. Chuẩn bị thư mục làm việc (Terminal, ngoài Claude Science)

Mở **Terminal**:

```bash
# 3.1 git (nếu chưa có; macOS sẽ hỏi cài Command Line Tools)
git --version || xcode-select --install

# 3.2 thư mục nghiên cứu
mkdir -p ~/research && cd ~/research

# 3.3 tải kho neur-v3 (khoảng 190 MB vì có dữ liệu thô của bài v2)
git clone https://github.com/DRuanli/neur-v3.git
cd neur-v3 && git log --oneline -1
```

Nếu kho riêng tư, git sẽ hỏi đăng nhập GitHub. Cách dễ nhất là cài GitHub CLI (`brew install gh`, rồi `gh auth login`); hoặc dùng Personal Access Token làm mật khẩu.

**Bố cục sau bước này:**

```
~/research/
├── neur-v3/            kho bài v3 (cấp cho Claude Science quyền Đọc & Ghi)
│   ├── _incoming/      kết quả Kaggle tải về (không vào git)
│   └── _bundles/       gói code gửi Kaggle (không vào git)
└── kaggle-cred/        khoá Kaggle API, chỉ khi dùng chế độ CLI (quyền Chỉ đọc; KHÔNG nằm trong kho)
```

## 4. Khoá Kaggle API (chỉ cần cho chế độ tự động; chế độ thủ công không cần)

1. kaggle.com → ảnh đại diện → **Settings** → mục **API** → tạo token mới.
2. Nếu trang tải về file `kaggle.json`:
   ```bash
   mkdir -p ~/research/kaggle-cred
   mv ~/Downloads/kaggle.json ~/research/kaggle-cred/
   chmod 600 ~/research/kaggle-cred/kaggle.json
   ```
   Nếu trang chỉ hiện một chuỗi token, làm theo hướng dẫn trên trang và báo Claude cách thầy đã lưu. **Không dán token vào cuộc trò chuyện.**
3. Kiểm trong Terminal (sau khi `pip install kaggle` ở một môi trường của thầy):
   ```bash
   KAGGLE_CONFIG_DIR=~/research/kaggle-cred kaggle kernels list --mine --page-size 5
   ```

Vì sao tách thư mục: sandbox của Claude Science chỉ thấy thư mục được cấp. Cấp riêng `kaggle-cred` ở chế độ **Chỉ đọc** thì khoá không bao giờ vào kho và Claude không sửa được nó.

## 5. Môi trường Python cho kho (Claude tạo trong Claude Science)

Không cần cài Python thủ công. Ở phiên đầu, prompt khởi đầu yêu cầu Claude tạo môi trường tên `neur-v3` gồm: numpy, scipy, pandas, scikit-learn, pytorch (bản CPU cho Apple Silicon), pytest, `tabicl==2.2.0`, `kaggle`. Mỗi lần cài, Claude Science hiện thẻ xin phép. Môi trường dùng chung cho mọi project trên máy.

Không cần cài TabPFN hay TabDPT trên máy: các TFM chỉ chạy trên Kaggle.

## 6. Các địa chỉ mạng thầy sẽ được hỏi (duyệt khi thẻ hiện ra)

| Địa chỉ | Để làm gì | Khi nào |
|---|---|---|
| `github.com` | `git pull` hoặc `git push` từ Claude | nếu thầy muốn Claude tự đồng bộ kho |
| `huggingface.co` và máy chủ tải file của nó | tải trọng số TabICL v2 để thử nhanh trên máy (không bắt buộc) | tuỳ chọn |
| `www.kaggle.com`, `storage.googleapis.com` | Kaggle CLI: tải gói lên, đẩy lượt chạy, tải output | chỉ ở chế độ CLI |
| `arxiv.org`, `export.arxiv.org`, `api.openalex.org` | tra tài liệu | khi tra tài liệu |

PyPI và conda được phép sẵn.

**Đẩy lên GitHub:** nếu `git push` từ trong Claude Science không đăng nhập được (sandbox không thấy keychain của macOS), thầy chạy `git push` trong Terminal. Có thể thử thêm GitHub token ở **Settings > Credentials**, nhưng tài liệu hiện tại không nói git trong sandbox dùng nó thế nào.

## 7. Kiểm tra cuối

- [ ] Claude Science mở được, đã đăng nhập, **Settings > Usage** hiện hạn mức.
- [ ] `~/research/neur-v3` có `CLAUDE.md`, `HANDOFF.md`, `v3/`, `code/`, `prior/`.
- [ ] (Chế độ CLI) lệnh kiểm Kaggle ở mục 4 chạy được.
- [ ] Đã có gói `claude-science-setup` em gửi, gồm hai skill dạng zip.

Tiếp theo: `02_TAO_PROJECT.md`.
