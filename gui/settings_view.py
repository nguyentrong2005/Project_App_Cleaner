# settings_view.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from gui.localization import tr, set_language, on_language_change

def build_settings_view(main_content):
    """
    Xây dựng giao diện tab 'Cài đặt' cho ứng dụng.

    Bao gồm các chức năng:
    - Chuyển đổi giữa giao diện sáng/tối (dark/light)
    - Thay đổi ngôn ngữ giữa Tiếng Việt và Tiếng Anh
    - Tự động cập nhật các label khi ngôn ngữ thay đổi

    Args:
        main_content: Frame cha nơi view này sẽ được gắn vào

    Returns:
        CTkFrame: Giao diện đã dựng sẵn cho tab 'Cài đặt'
    """
    f = ctk.CTkFrame(main_content)

    # Biến giao diện động
    title_var = tk.StringVar(value=tr("settings_title"))
    theme_label_var = tk.StringVar(value=tr("theme"))
    language_label_var = tk.StringVar(value=tr("language"))
    sound_label_var = tk.StringVar(value=tr("sound"))

    # Tiêu đề
    ctk.CTkLabel(f, textvariable=title_var, font=(
        "Segoe UI", 22, "bold")).pack(pady=20)

    # Container chứa các dòng setting
    container = ctk.CTkFrame(f, fg_color="transparent")
    container.pack(padx=40, pady=10)

    def change_theme(value):
        """
        Đổi giữa giao diện sáng / tối.

        Args:
            value (str): "Tối" hoặc "Sáng"
        """
        theme = "dark" if value == "Tối" else "light"
        ctk.set_appearance_mode(theme)

        # Cập nhật sidebar/panel nếu hàm có sẵn
        top = main_content.winfo_toplevel()
        if hasattr(top, "update_theme_colors"):
            top.update_theme_colors()

        messagebox.showinfo("Giao diện", f"Đã chuyển sang chế độ {value}")

    # Dòng: Chế độ giao diện
    ctk.CTkLabel(container, textvariable=theme_label_var, font=("Segoe UI", 14), anchor="w")\
        .grid(row=0, column=0, sticky="w", pady=10, padx=(0, 20))
    theme_menu = ctk.CTkOptionMenu(
        container, values=["Tối", "Sáng"], command=change_theme)
    theme_menu.set("Tối")
    theme_menu.grid(row=0, column=1, sticky="ew")

    # Ngôn ngữ
    lang_menu_var = tk.StringVar(value="Tiếng Việt")

    def change_language(value):
        """
        Thay đổi ngôn ngữ của toàn bộ ứng dụng.

        Args:
            value (str): "Tiếng Việt" hoặc "Tiếng Anh"
        """
        lang_code = "vi" if value == "Tiếng Việt" else "en"
        lang_menu_var.set(value)
        set_language(lang_code)

        # Gọi reload nếu app hỗ trợ
        top = main_content.winfo_toplevel()
        if hasattr(top, "reload_ui"):
            top.reload_ui()

    # Dòng: Ngôn ngữ
    ctk.CTkLabel(container, textvariable=language_label_var, font=("Segoe UI", 14), anchor="w")\
        .grid(row=1, column=0, sticky="w", pady=10, padx=(0, 20))
    lang_menu = ctk.CTkOptionMenu(container, values=["Tiếng Việt", "Tiếng Anh"],
                                  command=change_language, variable=lang_menu_var)
    lang_menu.grid(row=1, column=1, sticky="ew")

    # Cho cột bên phải dãn đều
    container.grid_columnconfigure(1, weight=1)

    def update_texts():
        """
        Cập nhật tất cả các label theo ngôn ngữ hiện tại.
        Được gọi tự động khi ngôn ngữ thay đổi.
        """
        title_var.set(tr("settings_title"))
        theme_label_var.set(tr("theme"))
        language_label_var.set(tr("language"))
        sound_label_var.set(tr("sound"))

    on_language_change(update_texts)

    return f
