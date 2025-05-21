# scan_view.py
import customtkinter as ctk
import tkinter as tk
import threading
import time
from gui.localization import tr, on_language_change
from controller.app_controller import scan_and_log_and_return
import os


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

    def show_file_classification(grouped):
        for widget in table_frame.winfo_children():
            widget.destroy()

        headers = ["Thư mục", "Số lượng", "Dung lượng"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(table_frame, text=h, font=("Segoe UI", 13, "bold"), text_color="#3b82f6")\
                .grid(row=0, column=i, padx=(10, 20), pady=(5, 8), sticky="w")

        for row, (folder, items) in enumerate(grouped.items(), start=1):
            size = 0
            for p in items:
                try:
                    size += p.stat().st_size
                except Exception:
                    pass

            ctk.CTkLabel(table_frame, text=str(folder), font=("Segoe UI", 12))\
                .grid(row=row, column=0, sticky="w", padx=10, pady=3)
            ctk.CTkLabel(table_frame, text=str(len(items)), font=("Segoe UI", 12))\
                .grid(row=row, column=1, sticky="w", padx=20)
            ctk.CTkLabel(table_frame, text=f"{size / 1024:.1f} KB", font=("Segoe UI", 12))\
                .grid(row=row, column=2, sticky="w", padx=20)

        table_frame.pack(padx=20, pady=(5, 20), fill="x")

    def start_scan():
        """
        Gọi quét rác thật từ backend và hiển thị kết quả
        """
        def run():
            # Reset UI trước khi quét
            result_label.configure(text="")
            progress_label.configure(text="🔍 Đang quét rác...")
            progress_bar.set(0.2)
            table_frame.pack_forget()

            # Gọi hàm quét và log thực
            grouped, total_size = scan_and_log_and_return()
            file_count = sum(len(lst) for lst in grouped.values())
            mb_size = total_size / (1024 * 1024)

            # Cập nhật giao diện
            time.sleep(0.5)
            progress_label.configure(text="✅ Quét hoàn tất")
            progress_bar.set(1.0)
            result_label.configure(
                text=f"Đã phát hiện {file_count} file/thư mục rác ({mb_size:.1f} MB)"
            )
            show_file_classification(grouped)

        threading.Thread(target=run, daemon=True).start()

    ctk.CTkButton(f, textvariable=start_btn_text,
                  command=start_scan, fg_color="#3b82f6").pack(pady=20)

    def update_texts():
        title_var.set(tr("scan_title"))
        desc_var.set(tr("scan_desc"))
        start_btn_text.set(tr("scan_start"))

    on_language_change(update_texts)

    return f
