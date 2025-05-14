import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

def build_settings_view(main_content):
    f = ctk.CTkFrame(main_content)
    ctk.CTkLabel(f, text="⚙️ Cài đặt ứng dụng", font=("Segoe UI", 22, "bold")).pack(pady=20)

    container = ctk.CTkFrame(f, fg_color="transparent")
    container.pack(padx=40, pady=10)

    # === Chế độ giao diện ===
    def change_theme(value):
        if value == "Tối":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        messagebox.showinfo("Đã thay đổi", f"Đã chuyển sang giao diện {value}")

    ctk.CTkLabel(container, text="🎨 Chế độ giao diện:", font=("Segoe UI", 14), anchor="w")\
        .grid(row=0, column=0, sticky="w", pady=10, padx=(0, 20))
    theme_menu = ctk.CTkOptionMenu(container, values=["Tối", "Sáng"], command=change_theme)
    theme_menu.set("Tối")
    theme_menu.grid(row=0, column=1, sticky="ew")

    # === Màu chủ đạo ===
    def change_color(value):
        messagebox.showinfo("Thông báo", f"Đã chọn màu chủ đạo: {value}\n(Chức năng sẽ áp dụng sau)")

    ctk.CTkLabel(container, text="🌈 Màu chủ đạo:", font=("Segoe UI", 14), anchor="w")\
        .grid(row=1, column=0, sticky="w", pady=10, padx=(0, 20))
    color_menu = ctk.CTkOptionMenu(container, values=["Xanh dương", "Xanh lá", "Đỏ", "Tím"], command=change_color)
    color_menu.set("Xanh dương")
    color_menu.grid(row=1, column=1, sticky="ew")

    # === Ngôn ngữ ===
    current_language = tk.StringVar(value="Tiếng Việt")

    def change_language(value):
        current_language.set(value)
        messagebox.showinfo("Đã thay đổi", f"Ngôn ngữ được chọn: {value}")

    ctk.CTkLabel(container, text="🌐 Ngôn ngữ:", font=("Segoe UI", 14), anchor="w")\
        .grid(row=2, column=0, sticky="w", pady=10, padx=(0, 20))
    lang_menu = ctk.CTkOptionMenu(container, values=["Tiếng Việt", "English"], command=change_language)
    lang_menu.set("Tiếng Việt")
    lang_menu.grid(row=2, column=1, sticky="ew")

    # === Âm thanh ===
    sound_state = tk.BooleanVar(value=True)

    def toggle_sound():
        messagebox.showinfo("Âm thanh", f"{'Đã bật' if sound_state.get() else 'Đã tắt'} âm thanh")

    ctk.CTkLabel(container, text="🔊 Âm thanh:", font=("Segoe UI", 14), anchor="w")\
        .grid(row=3, column=0, sticky="w", pady=10, padx=(0, 20))
    ctk.CTkSwitch(container, text="Bật/Tắt âm thanh", variable=sound_state, command=toggle_sound)\
        .grid(row=3, column=1, sticky="w")

    container.grid_columnconfigure(1, weight=1)
    return f
