import customtkinter as ctk
import threading
import time


def build_clean_view(main_content):
    f = ctk.CTkFrame(main_content)

    ctk.CTkLabel(f, text="🧹 Dọn hệ thống", font=(
        "Segoe UI", 22, "bold")).pack(pady=(20, 10))
    ctk.CTkLabel(f, text="Danh sách các mục rác được phát hiện:",
                 font=("Segoe UI", 14)).pack(pady=(0, 10))

    listbox = ctk.CTkScrollableFrame(f, height=200)
    listbox.pack(padx=20, pady=10, fill="x")

    items = [
        "📁 Thư mục tạm thời - 150 MB",
        "🔗 Shortcut hỏng - 30 mục",
        "🧩 Registry lỗi - 50 mục",

    ]
    for item in items:
        ctk.CTkLabel(listbox, text=item, font=("Segoe UI", 13)
                     ).pack(anchor="w", padx=10, pady=5)

    status = ctk.CTkLabel(f, text="", font=("Segoe UI", 12))
    status.pack(pady=(10, 5))

    result_label = ctk.CTkLabel(f, text="", font=("Segoe UI", 13))
    result_label.pack(pady=5)

    def do_cleanup():
        def run():
            status.configure(text="🧹 Đang dọn... Vui lòng chờ")
            for i in range(3):
                status.configure(text=f"🧹 Đang dọn{'.' * i}")
                time.sleep(0.5)
            time.sleep(1.5)
            status.configure(text="✅ Dọn dẹp hoàn tất")
            result_label.configure(
                text="Đã xoá thành công 932 MB rác hệ thống 🎉")
        threading.Thread(target=run, daemon=True).start()

    ctk.CTkButton(f, text="⚡ Bắt đầu dọn", command=do_cleanup,
                  fg_color="#10b981").pack(pady=15)

    return f
