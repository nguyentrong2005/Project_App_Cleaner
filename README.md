```markdown
# 🧹 CleanApp - Python System Cleaner

**CleanApp** là một ứng dụng dọn rác hệ thống viết bằng Python, sử dụng Tkinter làm giao diện người dùng. Ứng dụng hỗ trợ quét và xóa các file tạm, file không cần thiết nhằm giải phóng dung lượng ổ đĩa và cải thiện hiệu suất máy tính.

---

## 🚀 Tính năng

- Quét các thư mục chứa rác phổ biến:
  - `C:\Windows\Temp`
  - `%TEMP%`
  - Thùng rác (Recycle Bin)
- Hiển thị số lượng và dung lượng các file rác
- Cho phép xóa toàn bộ file rác chỉ với một nút bấm
- Giao diện người dùng thân thiện, dễ sử dụng

---

## 🖥️ Giao diện chính

> *(Thêm ảnh chụp màn hình vào thư mục `resources/` nếu có)*

---

## 🏗️ Cấu trúc thư mục

```

clean\_app/
├── main.py                    # Tập tin khởi động ứng dụng
├── gui/
│   └── main\_window\.py         # Giao diện Tkinter
├── controller/
│   └── app\_controller.py      # Điều phối GUI và dịch vụ
├── services/
│   ├── scanner.py             # Quét file rác
│   └── cleaner.py             # Xóa file rác
├── utils/
│   └── file\_utils.py          # Hàm tiện ích thao tác file
├── tests/
│   └── test\_cleaner.py        # Kiểm thử đơn vị
├── resources/
│   └── icons/                 # Icon hoặc ảnh chụp giao diện
└── README.md

````

---

## 📦 Cài đặt và chạy

### ✅ Yêu cầu hệ thống

- Python 3.10 trở lên
- Windows 10/11
- Các thư viện chuẩn: `tkinter`, `os`, `shutil`, `ctypes`, `send2trash` *(nếu dùng)*

### ⚙️ Cách chạy ứng dụng

```bash
git clone https://github.com/yourusername/clean_app.git
cd clean_app
python main.py
````

### 🚚 Đóng gói thành file thực thi (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

Sau khi chạy xong, file `.exe` sẽ nằm trong thư mục `dist/`.

---

## 🧪 Kiểm thử

```bash
cd tests
python test_cleaner.py
```

---

## 👨‍💻 Nhóm phát triển

| Họ tên     | Vai trò                       |
| ---------- | ----------------------------- |
| \[Tên bạn] | Trưởng nhóm, backend chính    |
| \[Tên A]   | Thiết kế giao diện            |
| \[Tên B]   | Controller và xử lý logic     |
| \[Tên C]   | Kiểm thử và viết hàm tiện ích |

---

## 📄 Giấy phép

Dự án dùng cho mục đích học tập và nghiên cứu. Không sử dụng cho mục đích thương mại.

---

## 📌 Ghi chú

* Luôn chạy app bằng quyền admin nếu cần dọn thư mục hệ thống
* Sao lưu dữ liệu quan trọng trước khi chạy bản release

```

---

Bạn chỉ cần:
1. Tạo file `README.md` trong thư mục `clean_app`.
2. Dán nội dung trên vào.
3. Sửa phần "Nhóm phát triển" bằng tên thật của nhóm bạn.
4. (Tùy chọn) Thêm ảnh giao diện vào `resources/icons/` và chèn link vào phần "🖥️ Giao diện chính".

Bạn có muốn mình tạo sẵn file `README.md` để tải trực tiếp không?
```
