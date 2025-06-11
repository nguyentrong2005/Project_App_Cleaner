# history_view.py
import customtkinter as ctk
import tkinter as tk
from gui.localization import tr, on_language_change
from controller.app_controller import get_clean_history
from utils.gui_helpers import show_detail_popup

_current_table_frame = None
_main_container = None

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
    global _current_table_frame, _main_container
    _main_container = main_content

    if _current_table_frame:
        _current_table_frame.destroy()
    
    f = ctk.CTkFrame(main_content)
    _current_table_frame = f

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

    history = get_clean_history()
    for time_str, summary_lines in history:
        if not summary_lines:
            continue

        main_info = summary_lines[0]
        count_text, size_text = main_info.split(", ")

        row = ctk.CTkFrame(table)
        row.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(row, text=time_str, anchor="w").pack(
            side="left", fill="x", expand=True)
        ctk.CTkLabel(row, text=count_text, width=80,
                     anchor="e").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=size_text, width=100,
                     anchor="e").pack(side="left")

        def open_detail(e, t=time_str, f=summary_lines):
            show_detail_popup(f"🧹 Đã xóa lúc {t}", f)

        row.bind("<Double-Button-1>", open_detail)
        for w in row.winfo_children():
            w.bind("<Double-Button-1>", open_detail)

    def update_texts():
        title_var.set(tr("history_title"))
        desc_var.set(tr("history_desc"))
        col_time_var.set(tr("history_col_time"))
        col_items_var.set(tr("history_col_items"))
        col_size_var.set(tr("history_col_size"))

    on_language_change(update_texts)

    return f

def refresh_history_view():
    if _main_container:
        build_history_view(_main_container)

