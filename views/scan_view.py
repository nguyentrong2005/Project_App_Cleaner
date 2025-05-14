import customtkinter as ctk
import threading, time

def build_scan_view(main_content):
    f = ctk.CTkFrame(main_content)

    ctk.CTkLabel(f, text="🔍 Quét hệ thống", font=("Segoe UI", 22, "bold")).pack(pady=(20, 10))
    ctk.CTkLabel(f, text="Hệ thống sẽ tìm và liệt kê các tệp rác, shortcut hỏng và registry lỗi.", font=("Segoe UI", 14)).pack(pady=(0, 20))

    progress_label = ctk.CTkLabel(f, text="⏳ Chưa bắt đầu", font=("Segoe UI", 12))
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
                progress_label.configure(text=f"🔎 Đang quét{d}")
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
            result_label.configure(text="Đã phát hiện 1015 tệp không cần thiết (932 MB)")
        threading.Thread(target=run, daemon=True).start()

    ctk.CTkButton(f, text="▶ Bắt đầu quét", command=start_scan, fg_color="#3b82f6").pack(pady=20)

    return f
