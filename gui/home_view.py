import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from gui.localization import tr, on_language_change
from core import get_system_info

PRIMARY_COLOR = "#3b82f6"
HOVER_BG = "#2a2e35"


def build_home_view(main_content, on_switch_view):
    """
    Xây dựng và trả về giao diện chính của màn hình Home trong ứng dụng.

    Giao diện bao gồm:
    - Tiêu đề và mô tả (theo ngôn ngữ hiện tại)
    - Đồng hồ thời gian thực góc trên phải
    - Một thẻ chức năng chính để chuyển sang màn hình quét rác
    - Nút "🖥 Xem hệ thống" để hiển thị thông tin thật của máy (CPU, RAM, ổ đĩa,...)
    - Mẹo nhỏ và khả năng cập nhật lại nội dung khi thay đổi ngôn ngữ

    Args:
        main_content: Widget cha (Frame) nơi chứa giao diện này
        on_switch_view: Hàm callback để chuyển đổi sang các màn hình khác

    Returns:
        CTkFrame: Giao diện trang Home hoàn chỉnh (CustomTkinter Frame)
    """
    home = ctk.CTkFrame(main_content)

    title_var = tk.StringVar(value=tr("home_title"))
    desc_var = tk.StringVar(value=tr("home_desc"))
    tip_var = tk.StringVar(value=tr("home_tip"))
    clean_text_var = tk.StringVar(value=tr("clean_title"))
    btn_sysinfo_text = tk.StringVar(value="🖥 Xem hệ thống")

    # Đồng hồ (hiển thị ở góc trên phải)
    clock_var = tk.StringVar()

    def update_clock():
        now = datetime.now()
        clock_var.set(now.strftime("🗓 %d/%m/%Y - 🕒 %H:%M:%S"))
        home.after(1000, update_clock)

    clock_label = ctk.CTkLabel(home, textvariable=clock_var, font=(
        "Segoe UI", 12), text_color="#aaa")
    clock_label.pack(anchor="ne", padx=20, pady=(10, 0))
    update_clock()

    # Tiêu đề và mô tả
    ctk.CTkLabel(home, textvariable=title_var, font=(
        "Segoe UI", 24, "bold"), anchor="center").pack(pady=(30, 10))
    ctk.CTkLabel(home, textvariable=desc_var, font=(
        "Segoe UI", 14), justify="center").pack(pady=(0, 30))

    # Thẻ chức năng chính
    card = ctk.CTkFrame(home, corner_radius=12, border_width=2,
                        border_color=PRIMARY_COLOR, height=150)
    card.pack(padx=80, pady=10, fill="x")

    row = ctk.CTkFrame(card, fg_color="transparent")
    row.pack(expand=True, fill="both", padx=20, pady=20)

    icon_label = ctk.CTkLabel(row, text="🧹", font=("Segoe UI", 48), width=80)
    icon_label.pack(side="left")

    text_label = ctk.CTkLabel(
        row, textvariable=clean_text_var, font=("Segoe UI", 20, "bold"))
    text_label.pack(side="left", padx=20)

    def on_enter(e):
        card.configure(border_color="#60a5fa", fg_color=HOVER_BG)

    def on_leave(e):
        card.configure(border_color=PRIMARY_COLOR, fg_color="transparent")

    def open_clean_view(event=None):
        on_switch_view("clean")

    for widget in [card, row, icon_label, text_label]:
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<Button-1>", open_clean_view)

    # Mẹo nhỏ
    ctk.CTkLabel(home, textvariable=tip_var, font=(
        "Segoe UI", 12), text_color="#aaa").pack(pady=(30, 10))

    # Khối thông tin hệ thống (ẩn/hiện)
    sysinfo_frame = ctk.CTkFrame(home, fg_color="transparent")
    sysinfo_label = ctk.CTkLabel(
        sysinfo_frame, font=("Segoe UI", 14), justify="left")
    sysinfo_label.pack()
    sysinfo_frame.pack_forget()

    def toggle_sysinfo():
        if sysinfo_frame.winfo_ismapped():
            sysinfo_frame.pack_forget()
        else:
            sysinfo_label.configure(text=get_system_info())
            sysinfo_frame.pack(pady=(10, 30))

    ctk.CTkButton(home, textvariable=btn_sysinfo_text,
                  command=toggle_sysinfo).pack(pady=(0, 10))

    # Cập nhật khi đổi ngôn ngữ
    def update_texts():
        title_var.set(tr("home_title"))
        desc_var.set(tr("home_desc"))
        tip_var.set(tr("home_tip"))
        clean_text_var.set(tr("clean_title"))
        btn_sysinfo_text.set("🖥 Xem hệ thống")

    on_language_change(update_texts)

    return home
