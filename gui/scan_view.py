# scan_view.py
import customtkinter as ctk
import tkinter as tk
import threading
import time
from localization import tr, on_language_change

def build_scan_view(main_content):
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

    def animate_text():
        dots = ["", ".", "..", "..."]
        for _ in range(20):
            for d in dots:
                progress_label.configure(text=f" {tr('scan_title')}{d}")
                time.sleep(0.15)

    def start_scan():
        def run():
            animate_thread = threading.Thread(target=animate_text)
            animate_thread.start()
            for i in range(101):
                progress_bar.set(i / 100)
                time.sleep(0.03)
            animate_thread.join()
            progress_label.configure(text="✅ Quét hoàn tất")
            result_label.configure(
                text="Đã phát hiện 1015 tệp không cần thiết (932 MB)")
        threading.Thread(target=run, daemon=True).start()

    ctk.CTkButton(f, textvariable=start_btn_text, command=start_scan,
                  fg_color="#3b82f6").pack(pady=20)

    def update_texts():
        title_var.set(tr("scan_title"))
        desc_var.set(tr("scan_desc"))
        start_btn_text.set(tr("scan_start"))

    on_language_change(update_texts)

    return f
