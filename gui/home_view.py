# home_view.py
import customtkinter as ctk
import tkinter as tk
from localization import tr, on_language_change

PRIMARY_COLOR = "#3b82f6"
HOVER_BG = "#2a2e35"  # nền khi hover

def build_home_view(main_content, on_switch_view):
    home = ctk.CTkFrame(main_content)

    # Dùng StringVar để thay đổi text linh hoạt
    title_var = tk.StringVar(value=tr("home_title"))
    desc_var = tk.StringVar(value=tr("home_desc"))
    tip_var = tk.StringVar(value=tr("home_tip"))

    ctk.CTkLabel(
        home,
        textvariable=title_var,
        font=("Segoe UI", 24, "bold"),
        anchor="center",
        justify="center"
    ).pack(pady=(40, 10))

    ctk.CTkLabel(
        home,
        textvariable=desc_var,
        font=("Segoe UI", 14),
        justify="center"
    ).pack(pady=(0, 30))

    card = ctk.CTkFrame(home, corner_radius=12, border_width=2,
                        border_color=PRIMARY_COLOR, height=150)
    card.pack(padx=80, pady=10, fill="x")

    row = ctk.CTkFrame(card, fg_color="transparent")
    row.pack(expand=True, fill="both", padx=20, pady=20)

    icon_label = ctk.CTkLabel(row, text="🧹", font=("Segoe UI", 48), width=80)
    icon_label.pack(side="left")

    clean_text_var = tk.StringVar(value=tr("clean_title"))
    text_label = ctk.CTkLabel(
        row, textvariable=clean_text_var, font=("Segoe UI", 20, "bold"))
    text_label.pack(side="left", padx=20)

    def on_enter(e):
        card.configure(border_color="#60a5fa", fg_color=HOVER_BG)

    def on_leave(e):
        card.configure(border_color=PRIMARY_COLOR, fg_color="transparent")

    for widget in [card, row, icon_label, text_label]:
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def open_clean_view(event=None):
        on_switch_view("clean")

    for widget in [card, row, icon_label, text_label]:
        widget.bind("<Button-1>", open_clean_view)

    ctk.CTkLabel(
        home,
        textvariable=tip_var,
        font=("Segoe UI", 12),
        text_color="#aaa"
    ).pack(pady=30)

    def update_texts():
        title_var.set(tr("home_title"))
        desc_var.set(tr("home_desc"))
        tip_var.set(tr("home_tip"))
        clean_text_var.set(tr("clean_title"))

    on_language_change(update_texts)

    return home
