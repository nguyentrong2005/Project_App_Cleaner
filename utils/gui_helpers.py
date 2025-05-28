# gui_helpers.py
import customtkinter as ctk
import tkinter as tk
import random
from gui.localization import tr


def show_detail_popup(title: str, files: list[str]):
    popup = ctk.CTkToplevel()
    popup.title(title)
    popup.geometry("600x400")
    popup.attributes("-topmost", True)

    # Căn giữa popup
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() - 600) // 2
    y = (popup.winfo_screenheight() - 400) // 2
    popup.geometry(f"+{x}+{y}")

    ctk.CTkLabel(popup, text=title, font=(
        "Segoe UI", 16, "bold")).pack(pady=10)

    # Header
    header = ctk.CTkFrame(popup, fg_color="transparent")
    header.pack(fill="x", padx=10, pady=(0, 5))
    ctk.CTkLabel(header, text=tr("detail_col_path"), anchor="w").pack(
        side="left", fill="x", expand=True)
    ctk.CTkLabel(header, text=tr("detail_col_size"),
                 width=100, anchor="e").pack(side="right")

    # List
    list_frame = ctk.CTkScrollableFrame(popup)
    list_frame.pack(fill="both", expand=True, padx=10, pady=5)
    show_more_btn = ctk.CTkButton(popup, text=tr("show_more"))

    displayed_count = tk.IntVar(value=0)
    total_files = len(files)
    step = 100

    def render_more():
        start = displayed_count.get()
        end = min(start + step, total_files)
        for fpath in files[start:end]:
            size = round(random.uniform(10, 500), 2)
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=fpath, anchor="w").pack(
                side="left", fill="x", expand=True)
            ctk.CTkLabel(row, text=f"{size} KB",
                         width=100, anchor="e").pack(side="right")
        displayed_count.set(end)

        if displayed_count.get() >= total_files:
            show_more_btn.pack_forget()
        else:
            show_more_btn.pack(pady=(0, 10))

    show_more_btn.configure(command=render_more)
    render_more()
