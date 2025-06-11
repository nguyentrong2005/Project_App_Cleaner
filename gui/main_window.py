import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os
from utils.safe_after import safe_after
import sys

from gui import (
    build_home_view,
    build_scan_view,
    build_history_view,
    build_settings_view,
    init_sidebar_labels,
    tr,
    on_language_change
)

PRIMARY_COLOR = "#3b82f6"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main_app():
    """
    Khởi tạo và chạy giao diện chính của ứng dụng T3K Cleaner.

    - Thiết lập cửa sổ chính, sidebar, nội dung và các nút điều hướng
    - Xử lý chuyển đổi giữa các view: home, scan, clean, settings, history
    - Tích hợp thay đổi ngôn ngữ và theme
    """
    app = ctk.CTk()
    app.title("T3K Cleaner")
    app.geometry("1100x600")

    app.active_button = None
    app.current_view = None
    app.button_refs = {}

    labels = init_sidebar_labels()

    try:
        app.iconbitmap(os.path.join(sys._MEIPASS, "assets", "images", "logo.ico") if hasattr(
            sys, "_MEIPASS") else "assets/images/logo.ico")
    except Exception as e:
        print("[Icon Error]", e)

    logo_img = None
    try:
        logo_path = os.path.join(sys._MEIPASS, "assets", "images", "logo.png") if hasattr(
            sys, "_MEIPASS") else "assets/images/logo.png"
        if os.path.exists(logo_path):
            logo_img = ctk.CTkImage(Image.open(logo_path), size=(32, 32))

    except Exception as e:
        print("[Logo Error]", e)

    def get_sidebar_color():
        return "#1f2937" if ctk.get_appearance_mode() == "Dark" else "transparent"

    # Sidebar trái
    app.sidebar = ctk.CTkFrame(
        app, width=220, corner_radius=0)
    app.sidebar.pack(side="left", fill="y")

    # Logo và tên app
    logo_frame = ctk.CTkFrame(app.sidebar, fg_color="transparent")
    logo_frame.pack(pady=(15, 10))
    if logo_img:
        ctk.CTkLabel(logo_frame, image=logo_img, text="").pack(
            side="left", padx=(5, 8))
    ctk.CTkLabel(logo_frame, text="T3K Cleaner", font=(
        "Segoe UI", 16, "bold")).pack(side="left")

    section_system_var = tk.StringVar(value="— " + tr("section_system") + " —")

    def section_title(var):
        return ctk.CTkLabel(app.sidebar, textvariable=var, font=("Segoe UI", 12, "bold"), text_color="#aaa")

    section_title(section_system_var).pack(anchor="w", padx=15, pady=(10, 0))

    def create_sidebar_button(label_var, key):
        """
        Tạo một nút điều hướng ở sidebar cho mỗi view.
        """
        btn = ctk.CTkButton(
            app.sidebar, textvariable=label_var, font=("Segoe UI", 14), anchor="w",
            fg_color="transparent", hover_color=PRIMARY_COLOR, corner_radius=8,
            command=lambda k=key: switch_view(k)
        )
        btn.bind("<Enter>", lambda e, b=btn: b.configure(
            fg_color=PRIMARY_COLOR) if b != app.active_button else None)
        btn.bind("<Leave>", lambda e, b=btn: b.configure(
            fg_color="transparent") if b != app.active_button else None)
        btn.pack(fill="x", padx=12, pady=4)
        app.button_refs[key] = btn

    for key in ["home", "scan",  "settings", "history"]:
        create_sidebar_button(labels[key], key)

    ctk.CTkButton(
        app.sidebar, textvariable=labels["exit"], font=("Segoe UI", 14), anchor="w",
        fg_color="#ef4444", hover_color="#dc2626", corner_radius=8,
        command=app.destroy
    ).pack(fill="x", padx=12, pady=(20, 5))

    # Nội dung chính
    main_wrapper = ctk.CTkFrame(app)
    main_wrapper.pack(side="left", fill="both", expand=True)

    app.main_content = ctk.CTkFrame(main_wrapper, corner_radius=0)
    app.main_content.pack(side="left", fill="both", expand=True)

    def set_active(btn):
        """
        Cập nhật nút sidebar đang được chọn.
        """
        if app.active_button:
            app.active_button.configure(fg_color="transparent")
        btn.configure(fg_color=PRIMARY_COLOR)
        app.active_button = btn

    def switch_view(name):
        """
        Chuyển đổi hiển thị giữa các view trong giao diện chính.
        """
        # Ẩn tất cả frame hiện tại
        for frame in views.values():
            frame.pack_forget()

        if name == "history":
            from gui.history_view import build_history_view, refresh_history_view
            refresh_history_view()
            views["history"] = build_history_view(
                app.main_content)  # tạo lại frame mới
            views["history"].pack(fill="both", expand=True)
        else:
            views[name].pack(fill="both", expand=True)

        set_active(app.button_refs[name])
        app.current_view = name

    # Danh sách các view
    views = {
        "home": build_home_view(app.main_content, switch_view),
        "scan": build_scan_view(app.main_content),
        # "history": build_history_view(app.main_content),
        "settings": build_settings_view(app.main_content),
    }

    def update_sidebar_texts():
        section_system_var.set("— " + tr("section_system") + " —")

    def update_theme_colors():
        """
        Cập nhật màu sidebar khi thay đổi giao diện sáng/tối.
        """
        is_dark = ctk.get_appearance_mode() == "Dark"
        sidebar_color = "#1f2937" if is_dark else "#ffffff"
        text_color = "#ffffff" if is_dark else "#000000"
        section_color = "#aaaaaa" if is_dark else "#555555"

        app.sidebar.configure(fg_color=sidebar_color)

        for btn in app.button_refs.values():
            btn.configure(text_color=text_color)

    app.update_theme_colors = update_theme_colors
    on_language_change(update_sidebar_texts)
    switch_view("home")
    set_active(app.button_refs["home"])
    app.mainloop()


def show_splash_screen():
    """
    Hiển thị splash screen khởi động với logo và hiệu ứng chấm.
    Tự động gọi main_app() sau vài giây.
    """
    splash = ctk.CTk()
    splash.geometry("300x200")
    splash.title("T3K Cleaner")
    icon_path = os.path.join(sys._MEIPASS, "assets", "images", "logo.ico") if hasattr(
        sys, "_MEIPASS") else "assets/images/logo.ico"
    splash.iconbitmap(icon_path)
    splash.overrideredirect(True)
    splash.eval('tk::PlaceWindow . center')

    frame = ctk.CTkFrame(splash, corner_radius=12)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    try:
        logo_path = os.path.join(sys._MEIPASS, "assets", "images", "logo.png") if hasattr(
            sys, "_MEIPASS") else "assets/images/logo.png"
        logo = ctk.CTkImage(Image.open(logo_path), size=(80, 80))
        ctk.CTkLabel(frame, image=logo, text="").pack(pady=(15, 10))
    except:
        pass

    loading_label = ctk.CTkLabel(
        frame, text="Đang khởi động", font=("Segoe UI", 14))
    loading_label.pack(pady=(10, 5))

    def animate_dots(i=0):
        if not splash.winfo_exists():
            return

        dots = ["", ".", "..", "..."]
        loading_label.configure(text=f"Đang khởi động{dots[i % 4]}")

        if i < 6:
            safe_after(splash, 500, animate_dots, i + 1)
        else:
            if splash.winfo_exists():
                splash.destroy()
            main_app()

    animate_dots()
    splash.mainloop()


def run_main_window():
    """
    Hàm để gọi giao diện chính từ file main.py.
    Gọi splash screen trước khi chạy ứng dụng.
    """
    show_splash_screen()
