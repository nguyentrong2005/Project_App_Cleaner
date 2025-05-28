# history_view.py
import customtkinter as ctk
import tkinter as tk
from gui.localization import tr, on_language_change
from controller.app_controller import get_scan_history


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
    col_time_var = tk.StringVar(value=tr("history_col_time"))
    col_items_var = tk.StringVar(value=tr("history_col_items"))
    col_size_var = tk.StringVar(value=tr("history_col_size"))

    header_row = ctk.CTkFrame(table, fg_color="transparent")
    header_row.pack(fill="x", padx=10, pady=(5, 8))

    ctk.CTkLabel(header_row, textvariable=col_time_var, font=(
        "Segoe UI", 13, "bold"), anchor="w").pack(side="left", fill="x", expand=True)
    ctk.CTkLabel(header_row, textvariable=col_items_var, font=(
        "Segoe UI", 13, "bold"), width=80, anchor="e").pack(side="left", padx=10)
    ctk.CTkLabel(header_row, textvariable=col_size_var, font=(
        "Segoe UI", 13, "bold"), width=100, anchor="e").pack(side="left")

    # Container lưu các dòng lịch sử, để dễ làm mới
    history_container = ctk.CTkFrame(table, fg_color="transparent")
    history_container.pack(fill="x", padx=10, pady=5)

    def render_history_data():
        # Xóa các dòng cũ
        for widget in history_container.winfo_children():
            widget.destroy()

        # Lấy lịch sử quét từ app_controller
        history = get_scan_history()
        for time_str, items, size in history:
            row = ctk.CTkFrame(history_container)
            row.pack(fill="x", padx=10, pady=2)

            ctk.CTkLabel(row, text=time_str, anchor="w").pack(
                side="left", fill="x", expand=True)
            ctk.CTkLabel(row, text=items, width=80,
                         anchor="e").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=size, width=100,
                         anchor="e").pack(side="left")


    def update_texts():
        title_var.set(tr("history_title"))
        desc_var.set(tr("history_desc"))
        col_time_var.set(tr("history_col_time"))
        col_items_var.set(tr("history_col_items"))
        col_size_var.set(tr("history_col_size"))
        render_history_data()

    on_language_change(update_texts)

    render_history_data()

    return f, render_history_data
