import customtkinter as ctk
import tkinter as tk
import psutil

from views.home_view import build_home_view
from views.scan_view import build_scan_view
from views.clean_view import build_clean_view
from views.history_view import build_history_view
from views.settings_view import build_settings_view

# Giao diện tổng thể
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def main_app():
    app = ctk.CTk()
    app.title("🧹 App Cleaner")
    app.geometry("1100x600")

    current_view = None
    active_button = None
    button_refs = {}

    # Sidebar trái
    sidebar = ctk.CTkFrame(app, width=220, corner_radius=0, fg_color="#1f2937")
    sidebar.pack(side="left", fill="y")

    ctk.CTkLabel(sidebar, text="🧹 App Cleaner", font=("Segoe UI", 16, "bold")).pack(pady=(15, 10))

    def section_title(text):
        return ctk.CTkLabel(sidebar, text=text, font=("Segoe UI", 12, "bold"), text_color="#aaa")

    section_title("— Hệ thống —").pack(anchor="w", padx=15, pady=(10, 0))

    # Hàm tạo nút sidebar
    def create_sidebar_button(text, key):
        btn = ctk.CTkButton(
            sidebar, text=text, font=("Segoe UI", 14), anchor="w",
            fg_color="transparent", hover_color="#3b82f6", corner_radius=8,
            command=lambda k=key: switch_view(k)
        )
        btn.bind("<Enter>", lambda e, b=btn: b.configure(fg_color="#3b82f6") if b != active_button else None)
        btn.bind("<Leave>", lambda e, b=btn: b.configure(fg_color="transparent") if b != active_button else None)
        btn.pack(fill="x", padx=12, pady=4)
        button_refs[key] = btn

    # Danh sách các nút
    for text, key in [
        ("🏠 Trang chủ", "home"),
        ("🔍 Quét", "scan"),
        ("🧹 Dọn", "clean"),
        ("⚙️ Cài đặt", "settings")
    ]:
        create_sidebar_button(text, key)

    section_title("— Thông tin —").pack(anchor="w", padx=15, pady=(15, 0))
    create_sidebar_button("📜 Lịch sử", "history")

    ctk.CTkButton(
        sidebar, text="❌ Thoát", font=("Segoe UI", 14), anchor="w",
        fg_color="#ef4444", hover_color="#dc2626", corner_radius=8,
        command=app.destroy
    ).pack(fill="x", padx=12, pady=(20, 5))

    # Khung chính chứa nội dung và info
    main_wrapper = ctk.CTkFrame(app)
    main_wrapper.pack(side="left", fill="both", expand=True)

    main_content = ctk.CTkFrame(main_wrapper, corner_radius=0)
    main_content.pack(side="left", fill="both", expand=True)

    sysinfo_panel = ctk.CTkFrame(main_wrapper, width=220)
    sysinfo_panel.pack(side="right", fill="y", padx=(0, 10), pady=10)

    sysinfo_title = ctk.CTkLabel(sysinfo_panel, text="🖥️ Thông tin hệ thống", font=("Segoe UI", 14, "bold"))
    sysinfo_title.pack(pady=(10, 20))

    # Cập nhật info hệ thống
    def update_sysinfo():
        cpu = psutil.cpu_percent()
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 1)
        used_ram = round(psutil.virtual_memory().used / (1024 ** 3), 1)

        info = [
            "🖥️ Windows 10",
            f"⚙️ CPU: {cpu}%",
            f"💾 RAM: {used_ram} / {ram} GB",
            "🧠 Intel Core i5",
            "🎮 NVIDIA GeForce"
        ]
        # Xoá cũ trước khi update
        for widget in sysinfo_panel.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget != sysinfo_title:
                widget.destroy()
        # Thêm mới
        for line in info:
            ctk.CTkLabel(sysinfo_panel, text=line, font=("Segoe UI", 12)).pack(pady=2, anchor="w", padx=10)

    # Các view
    views = {
        "home": build_home_view(main_content),
        "scan": build_scan_view(main_content),
        "clean": build_clean_view(main_content),
        "history": build_history_view(main_content),
        "settings": build_settings_view(main_content),
    }

    # Chuyển đổi giữa các view
    def set_active(btn):
        nonlocal active_button
        if active_button:
            active_button.configure(fg_color="transparent")
        btn.configure(fg_color="#3b82f6")
        active_button = btn

    def switch_view(name):
        nonlocal current_view
        for frame in views.values():
            frame.pack_forget()
        views[name].pack(fill="both", expand=True)
        update_sysinfo()
        set_active(button_refs[name])

    # Mặc định mở trang chủ
    switch_view("home")
    set_active(button_refs["home"])

    app.mainloop()

if __name__ == "__main__":
    main_app()
