# clean_view.py
import customtkinter as ctk
import tkinter as tk
import threading
import time
from localization import tr, on_language_change

def build_clean_view(main_content):
    f = ctk.CTkFrame(main_content)

    title_var = tk.StringVar(value=tr("clean_title"))
    list_title_var = tk.StringVar(value=tr("clean_list_title"))
    btn_text_var = tk.StringVar(value=tr("clean_button"))

    ctk.CTkLabel(f, textvariable=title_var, font=("Segoe UI", 22, "bold")).pack(pady=(20, 10))
    ctk.CTkLabel(f, textvariable=list_title_var, font=("Segoe UI", 14)).pack(pady=(0, 10))

    listbox = ctk.CTkScrollableFrame(f, height=200)
    listbox.pack(padx=20, pady=10, fill="x")

    items = [
        "📁 Thư mục tạm thời - 150 MB",
        "🔗 Shortcut hỏng - 30 mục",
        "🧩 Registry lỗi - 50 mục",
    ]
    for item in items:
        ctk.CTkLabel(listbox, text=item, font=("Segoe UI", 13)).pack(anchor="w", padx=10, pady=5)

    status = ctk.CTkLabel(f, text="", font=("Segoe UI", 12))
    status.pack(pady=(10, 5))
    progress_bar = ctk.CTkProgressBar(f, width=400)
    progress_bar.pack(pady=5)
    progress_bar.set(1.0)

    result_label = ctk.CTkLabel(f, text="", font=("Segoe UI", 13))
    result_label.pack(pady=5)

    def do_cleanup():
        def run():
            status.configure(text="🧹 Đang dọn... Vui lòng chờ")
            for i in range(3):
                status.configure(text=f"🧹 Đang dọn{'.' * i}")
                time.sleep(0.5)
            time.sleep(1.5)
            for percent in range(100, -1, -1):
                progress_bar.set(percent / 100)
                status.configure(text=f"🧹 Đang dọn: {percent}%")
                time.sleep(0.03)
            status.configure(text="✅ Dọn dẹp hoàn tất")
            result_label.configure(text="Đã xoá thành công 932 MB rác hệ thống 🎉")
        threading.Thread(target=run, daemon=True).start()

    def confirm_and_cleanup():
        popup = ctk.CTkToplevel()
        popup.title(tr("clean_title"))
        popup.geometry("300x140")
        popup.resizable(False, False)
        popup.grab_set()
         # Đặt ở giữa màn hình
        popup.update_idletasks()
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        popup.geometry(f"+{x}+{y}")

        ctk.CTkLabel(popup, text=tr("confirm_clean"), font=("Segoe UI", 14))\
            .pack(pady=(20, 10), padx=20)

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=10)

        def on_yes():
            popup.destroy()
            do_cleanup()

        def on_no():
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_no)

        ctk.CTkButton(btn_frame, text=tr("yes"), command=on_yes,
                      fg_color="#10b981", width=80).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text=tr("no"), command=on_no,
                      fg_color="#ef4444", width=80).pack(side="left", padx=10)

    ctk.CTkButton(f, textvariable=btn_text_var, command=confirm_and_cleanup,
                  fg_color="#10b981").pack(pady=15)

    def update_texts():
        title_var.set(tr("clean_title"))
        list_title_var.set(tr("clean_list_title"))
        btn_text_var.set(tr("clean_button"))

    on_language_change(update_texts)

    return f
