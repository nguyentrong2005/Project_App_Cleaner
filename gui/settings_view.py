# settings_view.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from localization import tr, set_language, on_language_change

def build_settings_view(main_content):
    f = ctk.CTkFrame(main_content)

    # Biến giao diện động
    title_var = tk.StringVar(value=tr("settings_title"))
    theme_label_var = tk.StringVar(value=tr("theme"))
    language_label_var = tk.StringVar(value=tr("language"))
    sound_label_var = tk.StringVar(value=tr("sound"))

    # Tiêu đề
    ctk.CTkLabel(f, textvariable=title_var, font=("Segoe UI", 22, "bold")).pack(pady=20)

    # Container chứa các dòng setting
    container = ctk.CTkFrame(f, fg_color="transparent")
    container.pack(padx=40, pady=10)

    # === Chế độ giao diện ===
    def change_theme(value):
        theme = "dark" if value == "Tối" else "light"
        ctk.set_appearance_mode(theme)

        # Gọi cập nhật màu cho sidebar và panel phải
        top = main_content.winfo_toplevel()
        if hasattr(top, "update_theme_colors"):
            top.update_theme_colors()

        messagebox.showinfo("Giao diện", f"Đã chuyển sang chế độ {value}")

    ctk.CTkLabel(container, textvariable=theme_label_var, font=("Segoe UI", 14), anchor="w")\
        .grid(row=0, column=0, sticky="w", pady=10, padx=(0, 20))
    theme_menu = ctk.CTkOptionMenu(container, values=["Tối", "Sáng"], command=change_theme)
    theme_menu.set("Tối")
    theme_menu.grid(row=0, column=1, sticky="ew")

    # === Ngôn ngữ ===
    lang_menu_var = tk.StringVar(value="Tiếng Việt")

    def change_language(value):
        lang_code = "vi" if value == "Tiếng Việt" else "en"
        lang_menu_var.set(value)
        set_language(lang_code)

        # Reload lại giao diện app
        top = main_content.winfo_toplevel()
        if hasattr(top, "reload_ui"):
            top.reload_ui()

    ctk.CTkLabel(container, textvariable=language_label_var, font=("Segoe UI", 14), anchor="w")\
        .grid(row=1, column=0, sticky="w", pady=10, padx=(0, 20))
    lang_menu = ctk.CTkOptionMenu(container, values=["Tiếng Việt", "Tiếng Anh"],
                                  command=change_language, variable=lang_menu_var)
    lang_menu.grid(row=1, column=1, sticky="ew")

    

    # Cho cột 1 (bên phải) dãn ra đều
    container.grid_columnconfigure(1, weight=1)

    # === Khi đổi ngôn ngữ, cập nhật label
    def update_texts():
        title_var.set(tr("settings_title"))
        theme_label_var.set(tr("theme"))
        language_label_var.set(tr("language"))
        sound_label_var.set(tr("sound"))

    on_language_change(update_texts)

    return f
