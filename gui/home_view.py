import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from gui.localization import tr, on_language_change
from controller.app_controller import get_system_info
from utils.safe_after import safe_after


PRIMARY_COLOR = "#3b82f6"
HOVER_BG = "#2a2e35"


def build_home_view(main_content, on_switch_view):
    home = ctk.CTkFrame(main_content)

    title_var = tk.StringVar(value=tr("home_title"))
    desc_var = tk.StringVar(value=tr("home_desc"))
    tip_var = tk.StringVar(value=tr("home_tip"))
    clean_text_var = tk.StringVar(value=tr("clean_title"))
    btn_sysinfo_text = tk.StringVar(value=tr("home_system"))
    clock_var = tk.StringVar()

    # ====== HÀM MÀU THEO GIAO DIỆN ======
    
    def get_hover_bg():
        return "black" if ctk.get_appearance_mode().lower() == "dark" else "white"


    # ====== ĐỒNG HỒ GÓC PHẢI ======
    def update_clock():
        if not home.winfo_exists():
            return
        now = datetime.now()
        clock_var.set(now.strftime(" %d/%m/%Y -  %H:%M:%S"))
        safe_after(home, 1000, update_clock)

    clock_label = ctk.CTkLabel(home, textvariable=clock_var, font=("Segoe UI", 12),
                               )
    clock_label.pack(anchor="ne", padx=20, pady=(10, 0))
    update_clock()

    # ====== TIÊU ĐỀ & MÔ TẢ ======
    ctk.CTkLabel(home, textvariable=title_var, font=("Segoe UI", 24, "bold"),
                 anchor="center").pack(pady=(30, 10))
    ctk.CTkLabel(home, textvariable=desc_var, font=("Segoe UI", 14),
                 justify="center").pack(pady=(0, 30))

    # ====== THẺ CHỨC NĂNG CHÍNH (QUÉT RÁC) ======
    card = ctk.CTkFrame(home, corner_radius=12, border_width=2,
                        border_color=PRIMARY_COLOR, height=150)
    card.pack(padx=80, pady=10, fill="x")

    row = ctk.CTkFrame(card, fg_color="transparent")
    row.pack(expand=True, fill="both", padx=20, pady=20)

    icon_label = ctk.CTkLabel(row, text="🧹", font=("Segoe UI", 48), width=80)
    icon_label.pack(side="left")

    text_label = ctk.CTkLabel(row, textvariable=clean_text_var,
                              font=("Segoe UI", 20, "bold"))
    text_label.pack(side="left", padx=20)

    def on_enter(e):
        card.configure(fg_color=get_hover_bg())

    def on_leave(e):
        card.configure(fg_color="transparent")

    def open_scan_view(event=None):
        on_switch_view("scan")

    for widget in [card, row, icon_label, text_label]:
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<Button-1>", open_scan_view)

    # ====== MẸO NHỎ ======
    tip_label = ctk.CTkLabel(home, textvariable=tip_var, font=("Segoe UI", 12),
                             )
    tip_label.pack(pady=(30, 10))

    # ====== THÔNG TIN HỆ THỐNG ======
    sysinfo_frame = ctk.CTkFrame(home)
    sysinfo_label = ctk.CTkLabel(sysinfo_frame, font=("Segoe UI", 14), justify="left")
    sysinfo_label.pack()
    sysinfo_frame.pack_forget()

    def toggle_sysinfo():
        if sysinfo_frame.winfo_ismapped():
            sysinfo_frame.pack_forget()
        else:
            info = get_system_info()
            sysinfo_label.configure(text=info)
            sysinfo_frame.pack(pady=(10, 30))

    ctk.CTkButton(home, textvariable=btn_sysinfo_text,
                  command=toggle_sysinfo).pack(pady=(0, 10))

    # ====== CẬP NHẬT KHI ĐỔI NGÔN NGỮ ======
    def update_texts():
        title_var.set(tr("home_title"))
        desc_var.set(tr("home_desc"))
        tip_var.set(tr("home_tip"))
        clean_text_var.set(tr("clean_title"))
        btn_sysinfo_text.set(tr("home_system"))

    on_language_change(update_texts)

    

    return home
