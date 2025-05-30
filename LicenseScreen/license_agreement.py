import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Không tìm thấy nội dung."

def show_text_popup(title, file_path):
    content = read_file(file_path)
    popup = ctk.CTkToplevel()
    popup.title(title)
    popup.geometry("600x400")

    label = ctk.CTkLabel(popup, text=title, font=ctk.CTkFont(size=16, weight="bold"))
    label.pack(pady=10)

    textbox = ctk.CTkTextbox(popup, wrap="word", width=560, height=300)
    textbox.insert("1.0", content)
    textbox.configure(state="disabled")
    textbox.pack(padx=10, pady=10)

    ctk.CTkButton(popup, text="Đóng", command=popup.destroy).pack(pady=10)

def show_license_screen(on_accept):
    window = ctk.CTk()
    window.title("Điều khoản sử dụng – App Cleaner")
    window.geometry("500x300")
    window.resizable(False, False)

    label = ctk.CTkLabel(window, text="Vui lòng đọc và đồng ý để sử dụng App Cleaner", font=ctk.CTkFont(size=16, weight="bold"))
    label.pack(pady=15)

    ctk.CTkButton(window, text="📜 Thỏa thuận người dùng", command=lambda: show_text_popup("Thỏa thuận người dùng", "eula.txt")).pack(pady=5)
    ctk.CTkButton(window, text="🔒 Chính sách bảo mật", command=lambda: show_text_popup("Chính sách bảo mật", "privacy.txt")).pack(pady=5)

    btn_frame = ctk.CTkFrame(window)
    btn_frame.pack(pady=20)

    def agree():
        window.destroy()
        on_accept()

    def disagree():
        window.destroy()
        sys.exit()

    ctk.CTkButton(btn_frame, text="Tôi đồng ý", command=agree, width=120).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Thoát", command=disagree, fg_color="gray").pack(side="left", padx=10)

    window.mainloop()



