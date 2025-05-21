# scan_view.py
import customtkinter as ctk
import tkinter as tk
import threading
import time
from gui.localization import tr, on_language_change


def build_scan_view(main_content):
    """
    Xây dựng giao diện chức năng 'Quét hệ thống' cho ứng dụng Cleaner.

    Giao diện bao gồm:
    - Tiêu đề và mô tả quét
    - Nút bắt đầu quét (mô phỏng)
    - Thanh tiến trình hiển thị các bước quét
    - Kết quả số lượng file rác phát hiện được
    - Bảng phân loại file rác (tạm, shortcut, cache, log, registry...)

    Args:
        main_content: Frame cha nơi view sẽ được hiển thị

    Returns:
        CTkFrame: Giao diện CTkFrame đã dựng sẵn
    """
    f = ctk.CTkFrame(main_content)

    title_var = tk.StringVar(value=tr("scan_title"))
    desc_var = tk.StringVar(value=tr("scan_desc"))
    start_btn_text = tk.StringVar(value=tr("scan_start"))

    ctk.CTkLabel(f, textvariable=title_var, font=(
        "Segoe UI", 22, "bold")).pack(pady=(20, 10))
    ctk.CTkLabel(f, textvariable=desc_var, font=(
        "Segoe UI", 14)).pack(pady=(0, 20))

    progress_label = ctk.CTkLabel(
        f, text="⏳ Chưa bắt đầu", font=("Segoe UI", 12))
    progress_label.pack(pady=(10, 5))

    progress_bar = ctk.CTkProgressBar(f, width=400)
    progress_bar.pack(pady=10)
    progress_bar.set(0)

    result_label = ctk.CTkLabel(f, text="", font=("Segoe UI", 13))
    result_label.pack(pady=10)

    table_frame = ctk.CTkScrollableFrame(f, height=220)
    table_frame.pack(padx=20, pady=(5, 20), fill="x")
    table_frame.pack_forget()

    def show_file_classification():
        """
        Hiển thị bảng thống kê các loại file rác sau khi quét xong.
        Dữ liệu hiện tại là giả lập.
        """
        for widget in table_frame.winfo_children():
            widget.destroy()

        headers = ["Loại file", "Số lượng", "Dung lượng"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(table_frame, text=h, font=("Segoe UI", 13, "bold"), text_color="#3b82f6")\
                .grid(row=0, column=i, padx=(10, 20), pady=(5, 8), sticky="w")

        data = [
            ("📁 Thư mục tạm thời", "310", "250 MB"),
            ("🔗 Shortcut hỏng", "48", "20 MB"),
            ("🧩 Registry lỗi", "112", "5 MB"),
            ("🧹 Cache trình duyệt", "206", "180 MB"),
            ("📄 File log", "94", "35 MB"),
        ]
        for row, (name, count, size) in enumerate(data, start=1):
            ctk.CTkLabel(table_frame, text=name, font=("Segoe UI", 13))\
                .grid(row=row, column=0, sticky="w", padx=10, pady=3)
            ctk.CTkLabel(table_frame, text=count, font=("Segoe UI", 13))\
                .grid(row=row, column=1, sticky="w", padx=20)
            ctk.CTkLabel(table_frame, text=size, font=("Segoe UI", 13))\
                .grid(row=row, column=2, sticky="w", padx=20)

        table_frame.pack(padx=20, pady=(5, 20), fill="x")

    def start_scan():
        """
        Mô phỏng quá trình quét hệ thống:
        - Hiển thị từng bước quét với hiệu ứng chấm
        - Cập nhật thanh tiến trình
        - Hiện kết quả và gọi hiển thị bảng phân loại file
        """
        def run():
            result_label.configure(text="")
            table_frame.pack_forget()

            steps = [
                "Đang kiểm tra thư mục tạm thời",
                "Đang quét shortcut hỏng",
                "Đang quét registry lỗi",
                "Đang phân tích file hệ thống",
                "Đang tính toán dung lượng rác"
            ]

            for idx, text in enumerate(steps):
                for dot in ["", ".", "..", "..."]:
                    progress_label.configure(text=f"🔍 {text}{dot}")
                    time.sleep(0.2)
                progress_bar.set((idx + 1) / len(steps))

            progress_label.configure(text="✅ Quét hoàn tất")
            result_label.configure(
                text="Đã phát hiện 1015 tệp không cần thiết (932 MB)")
            show_file_classification()

        threading.Thread(target=run, daemon=True).start()

    ctk.CTkButton(f, textvariable=start_btn_text,
                  command=start_scan, fg_color="#3b82f6").pack(pady=20)

    def update_texts():
        title_var.set(tr("scan_title"))
        desc_var.set(tr("scan_desc"))
        start_btn_text.set(tr("scan_start"))

    on_language_change(update_texts)

    return f
