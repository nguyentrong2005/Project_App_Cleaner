import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

def build_settings_view(main_content):
    f = ctk.CTkFrame(main_content)

    ctk.CTkLabel(f, text="⚙️ Cài đặt ứng dụng", font=("Segoe UI", 22, "bold")).pack(pady=20)

    # Giao diện
    ctk.CTkLabel(f, text="🎨 Chế độ giao diện:", font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(10, 5))
    def change_theme(value):
        ctk.set_appearance_mode(value.lower())
        messagebox.showinfo("Đã thay đổi", f"Đã chuyển sang giao diện {value}")

    theme_menu = ctk.CTkOptionMenu(f, values=["Dark", "Light"], command=change_theme)
    theme_menu.set("Dark")
    theme_menu.pack(padx=20, pady=5)

    # Màu chủ đạo
    ctk.CTkLabel(f, text="🌈 Màu chủ đạo:", font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(15, 5))
    def change_color(value):
        messagebox.showinfo("Thông báo", f"Đã chọn màu chủ đạo: {value}\n(Chức năng sẽ áp dụng sau)")

    ctk.CTkOptionMenu(f, values=["Xanh dương", "Xanh lá", "Đỏ", "Tím"], command=change_color).pack(padx=20, pady=5)

    # Ngôn ngữ
    ctk.CTkLabel(f, text="🌐 Ngôn ngữ:", font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(15, 5))
    current_language = tk.StringVar(value="Tiếng Việt")
    def change_language(value):
        current_language.set(value)
        messagebox.showinfo("Đã thay đổi", f"Ngôn ngữ được chọn: {value}")

    lang_menu = ctk.CTkOptionMenu(f, values=["Tiếng Việt", "English"], command=change_language)
    lang_menu.set("Tiếng Việt")
    lang_menu.pack(padx=20, pady=5)

    # Âm thanh
    ctk.CTkLabel(f, text="🔊 Âm thanh:", font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(15, 5))
    sound_state = tk.BooleanVar(value=True)
    def toggle_sound():
        messagebox.showinfo("Âm thanh", f"{'Đã bật' if sound_state.get() else 'Đã tắt'} âm thanh")

    ctk.CTkSwitch(f, text="Bật/Tắt âm thanh", variable=sound_state, command=toggle_sound).pack(padx=20, pady=5)

    return f
