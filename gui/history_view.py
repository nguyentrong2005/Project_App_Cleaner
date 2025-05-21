# history_view.py
import customtkinter as ctk
import tkinter as tk
from gui.localization import tr, on_language_change


def build_history_view(main_content):
    """
    Xây dựng giao diện tab 'Lịch sử' cho ứng dụng Cleaner.

    Giao diện hiển thị:
    - Tiêu đề và mô tả (tùy theo ngôn ngữ)
    - Bảng liệt kê các phiên dọn rác đã thực hiện (thời gian, số mục, dung lượng)
    - Dữ liệu hiện tại là giả lập, nhưng có thể thay bằng dữ liệu thực từ file hoặc database
    - Hỗ trợ tự động cập nhật nội dung khi thay đổi ngôn ngữ

    Args:
        main_content: Frame cha chứa toàn bộ nội dung giao diện này

    Returns:
        CTkFrame: Giao diện đã dựng sẵn cho tab 'History'
    """
    f = ctk.CTkFrame(main_content)

    title_var = tk.StringVar(value=tr("history_title"))
    desc_var = tk.StringVar(value=tr("history_desc"))

    ctk.CTkLabel(f, textvariable=title_var, font=(
        "Segoe UI", 22, "bold")).pack(pady=(20, 10))
    ctk.CTkLabel(f, textvariable=desc_var, font=(
        "Segoe UI", 14)).pack(pady=(0, 10))

    table = ctk.CTkScrollableFrame(f, height=250)
    table.pack(padx=20, pady=10, fill="x")

    # Tiêu đề cột
    headers = ("🕒 Thời gian", "🧹 Số mục", "💾 Dung lượng")
    header_text = f"{headers[0]:<25}{headers[1]:<15}{headers[2]}"
    ctk.CTkLabel(table, text=header_text, font=("Segoe UI", 13, "bold"),
                 text_color="#3b82f6").pack(anchor="w", padx=(10, 20), pady=(5, 8))

    # Dữ liệu lịch sử mẫu (giả lập)
    history = [
        ("2025-05-07 14:32", "5 mục", "420 MB"),
        ("2025-05-06 11:20", "8 mục", "932 MB"),
        ("2025-05-01 09:02", "6 mục", "750 MB"),
    ]
    for time_str, items, size in history:
        line = f"{time_str:<25}{items:<15}{size}"
        ctk.CTkLabel(table, text=line, font=("Segoe UI", 13)
                     ).pack(anchor="w", padx=20, pady=3)

    def update_texts():
        title_var.set(tr("history_title"))
        desc_var.set(tr("history_desc"))

    on_language_change(update_texts)

    return f
