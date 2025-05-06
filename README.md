
# 🧹 CleanApp - Ứng dụng dọn rác máy tính bằng Python

CleanApp là một ứng dụng đơn giản giúp người dùng quét và xóa các tập tin rác, tập tin tạm trên hệ thống Windows để giải phóng dung lượng và tăng hiệu suất hoạt động. Ứng dụng được viết bằng Python và sử dụng thư viện `tkinter` cho giao diện đồ họa (GUI).

---

## 🔍 Tổng Quan

CleanApp hỗ trợ người dùng:
- Quét các thư mục chứa file rác phổ biến trên Windows như `Temp`, `Prefetch`, `Recycle Bin`, v.v.
- Hiển thị danh sách và tổng dung lượng các file rác tìm được
- Xóa các file rác chỉ với một cú nhấp chuột
- Giao diện trực quan, dễ sử dụng cho cả người không rành công nghệ

Ứng dụng hoạt động tốt trên **Windows 10/11**, yêu cầu **Python 3.10 trở lên**.

---

## 📌 Yêu Cầu

Trước khi chạy chương trình, bạn cần đảm bảo đã cài đặt Python và (nếu cần) các thư viện ngoài bằng lệnh:

```bash
pip install send2trash
```

---

## 📂 Cấu Trúc Thư Mục

```
clean_app/
├── main.py                    # Khởi chạy ứng dụng
├── gui/
│   └── main_window.py         # Giao diện người dùng
├── controller/
│   └── app_controller.py      # Xử lý logic giữa GUI và services
├── services/
│   ├── scanner.py             # Quét các file rác
│   └── cleaner.py             # Xóa file rác
├── utils/
│   └── file_utils.py          # Hàm tiện ích chung
├── tests/
│   └── test_cleaner.py        # Kiểm thử chức năng xóa file
├── resources/
│   └── icons/                 # Icon, ảnh dùng trong giao diện
├── README.md                  # Tài liệu mô tả dự án
└── requirements.txt           # Danh sách thư viện cần cài
```

---

## 🚀 Chạy Ứng Dụng

Để chạy CleanApp, bạn thực hiện các bước sau:

```bash
git clone https://github.com/yourusername/CleanApp.git
cd CleanApp
python main.py
```

> Nếu muốn đóng gói thành `.exe`:
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

---

## 🧪 Kiểm Thử

```bash
cd tests
python test_cleaner.py
```

---

## 👨‍💻 Nhóm Phát Triển

| Họ Tên         | Vai Trò                       |
|----------------|-------------------------------|
| [Tên Bạn]      | Trưởng nhóm, xử lý backend    |
| [Tên Thành viên A] | Thiết kế giao diện GUI     |
| [Tên Thành viên B] | Controller và xử lý logic  |
| [Tên Thành viên C] | Kiểm thử và viết tiện ích  |

---

## 📄 Giấy Phép

Dự án được phát triển cho mục đích học tập, không dùng cho thương mại. Chi tiết xem file [LICENSE.md](LICENSE) (nếu có).

---

## 📌 Ghi chú

- Ứng dụng nên chạy bằng quyền Administrator để truy cập và xóa các thư mục hệ thống.
- Đảm bảo không mở ứng dụng hệ thống (như Recycle Bin) khi đang xóa rác để tránh lỗi truy cập.
