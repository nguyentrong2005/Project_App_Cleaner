# 🧹 CleanerApp – Ứng dụng dọn rác hệ thống Windows bằng Python

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)
![License](https://img.shields.io/badge/License-Free-green)
![Status](https://img.shields.io/badge/Build-Stable-brightgreen)

CleanerApp là một ứng dụng mã nguồn mở được phát triển bằng Python nhằm hỗ trợ người dùng Windows quét và xóa các **tệp tin rác** và **thư mục tạm** một cách an toàn, nhanh chóng và hiệu quả. Ứng dụng có giao diện thân thiện, đa ngôn ngữ, hiển thị tiến trình và lưu lịch sử rõ ràng.

---

## 🎯 Mục tiêu

- Giúp người dùng giải phóng bộ nhớ, tăng hiệu suất hệ thống Windows.
- Dọn dẹp các file rác, file tạm, cache trình duyệt, thư mục rỗng, v.v.
- Trải nghiệm GUI với **Tkinter**, thao tác hệ thống, xử lý file và kiểm thử phần mềm.

---

## 🧩 Chức năng nổi bật

- ✅ **Quét hệ thống đa luồng** để tìm và phân loại rác
- ✅ **Xóa an toàn** (kiểm tra quyền ghi, khóa file)
- ✅ **Phân loại rác thành 12 nhóm chính**
- ✅ **Hiển thị chi tiết quét**: số file, tổng dung lượng, thời gian quét
- ✅ **Giao diện hiện đại** với nút `Quét`, `Dọn`, `Thoát`, trạng thái thời gian thực
- ✅ **Hỗ trợ đa ngôn ngữ**: Tiếng Việt / English
- ✅ **Ghi lại lịch sử** dọn rác và chi tiết file đã xử lý
- ✅ **Đóng gói `.exe`** và có **bộ cài đặt (.exe installer)** với Inno Setup

---

## 🧹 Danh sách 12 loại rác có thể quét

Ứng dụng tự động phân loại các loại rác sau:

| # | Loại rác                 | Mô tả                                                                 |
|---|---------------------------|----------------------------------------------------------------------|
| 1 | Internet cache           | Bộ nhớ tạm của trình duyệt (Chrome, Edge, Firefox...)               |
| 2 | Cookies                  | File lưu session, theo dõi người dùng trong trình duyệt             |
| 3 | Internet history         | Lịch sử truy cập trình duyệt                                         |
| 4 | Metrics temp file        | File theo dõi, telemetry từ hệ điều hành                            |
| 5 | Temporary internet files | Tệp tạm khi duyệt web, lưu nội dung trang                           |
| 6 | Thumbnail cache          | Ảnh xem trước (thumbnail) được hệ thống cache lại                   |
| 7 | Empty recycle bin        | Dọn sạch thùng rác                                                   |
| 8 | Temporary files          | File có đuôi `.tmp`, `.temp`, `.~`,... hoặc dung lượng = 0          |
| 9 | Memory dumps             | File `.dmp`, lưu snapshot khi hệ thống crash                        |
|10 | Windows log files        | File `.log` do Windows tạo trong logs, debug                        |
|11 | Windows web cache        | Các cache đặc biệt của Windows như `webcache`, `cache2`,...         |
|12 | Microsoft OneDrive       | File cache/sync chưa hoàn thiện từ OneDrive                         |

Các file không xác định được sẽ vào nhóm “**Khác**” và vẫn có thể xóa nếu được chọn.

---

## ⚙️ Cơ chế hoạt động

### 1. **Quét rác**
- Quét các thư mục phổ biến như:
  - `C:/Windows/Temp`
  - `%TEMP%`
  - `$Recycle.Bin`
  - `AppData/Local`, `AppData/Roaming`
  - Thư mục `Downloads`
  - Cache các trình duyệt đã cài: Chrome, Edge, Firefox...
- Duyệt bằng **đa luồng**, giới hạn độ sâu thư mục để tăng tốc.
- Tự động phân loại 12 nhóm rác nêu trên.

### 2. **Xóa rác**
- Kiểm tra quyền xóa (`delete`, `write`) và trạng thái khóa file.
- Xóa file hoặc thư mục rỗng.
- Ghi lại lịch sử xóa vào:
  - `docs/cleaner/history_cleaner.txt` (tổng quan)
  - `docs/cleaner/chi_tiet_xoa/*.txt` (chi tiết từng file)

---

## 🖼️ Giao diện người dùng

- Giao diện hiện đại (CustomTkinter)
- Nút thao tác rõ ràng: `Quét`, `Dọn`, `Thoát`
- Hiển thị tiến trình quét, thời gian thực hiện
- Cho phép xem chi tiết từng nhóm rác (double click)
- Giao diện **đa ngôn ngữ**, chuyển đổi tức thì giữa **Tiếng Việt** và **English**

---

## 🏗️ Kiến trúc dự án

```
CleanerApp/
├── core/             # Xử lý quét, xóa, phân loại
├── controller/       # Liên kết logic giữa GUI và xử lý
├── gui/              # Giao diện người dùng
├── utils/            # Hàm tiện ích kiểm tra khóa, quyền
├── docs/             # Lưu lịch sử, license, điều khoản,...
├── assets/           # Hình ảnh, icon ứng dụng
├── main.py           # Tập tin khởi chạy chính
└── build_cleaner.bat # File batch đóng gói pyinstaller
```

---

## 🚀 Cài đặt & sử dụng

### 1. Cài thư viện
```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng
```bash
python main.py
```

### 3. Đóng gói `.exe`
```bash
pyinstaller --noconfirm --onefile --windowed main.py
```

### 4. Tạo trình cài đặt
- Mở `installer_script.iss` bằng **Inno Setup 6.4.3**
- Build ra file `CleanerAppInstaller.exe`

---

## 🧪 Kiểm thử

- Viết test thủ công và tự động
- Kiểm tra quyền truy cập, trạng thái khóa
- Xem lại lịch sử xóa tại thư mục: `docs/cleaner/chi_tiet_xoa/`

---

## 👨‍💻 Nhóm phát triển

| Thành viên              | Vai trò                    | Công việc chính |
|-------------------------|-----------------------------|------------------|
| **Nguyễn Hữu Trọng**    | Trưởng nhóm, Backend        | Quét/xóa rác, cấu trúc hệ thống, tích hợp toàn bộ |
| **Cái Trần Đăng Khôi**  | Giao diện, Demo             | Thiết kế GUI chính, trạng thái, slide và video demo |
| **Nguyễn Huỳnh Tường**  | Controller & logic          | Kết nối các nút giao diện với xử lý quét/xóa |
| **Huỳnh Thanh Trình**   | Tiện ích, Kiểm thử          | Kiểm tra khóa file, viết test, log chi tiết xóa |

---

## 📄 License

Dự án phi thương mại – chỉ phục vụ mục đích học tập, nghiên cứu.  
Thông tin chi tiết nằm trong các file `docs/license_agreement_*.txt`.

---

## 📌 Lưu ý

- **Nên chạy ứng dụng bằng quyền Administrator** để có thể xóa các thư mục hệ thống.
- Không nên mở các ứng dụng như Recycle Bin khi đang quét/xóa để tránh lỗi quyền truy cập.