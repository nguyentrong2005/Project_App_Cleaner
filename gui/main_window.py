# main_window.py
import customtkinter as ctk
import tkinter as tk
import psutil
from PIL import Image
import os

from home_view import build_home_view
from scan_view import build_scan_view
from clean_view import build_clean_view
from history_view import build_history_view
from settings_view import build_settings_view
from sidebar_labels import init_sidebar_labels
from localization import tr, on_language_change

PRIMARY_COLOR = "#3b82f6"
SUCCESS_COLOR = "#10b981"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def main_app():
    app = ctk.CTk()
    app.title("T3K Cleaner")
    app.geometry("1100x600")

    labels = init_sidebar_labels()

    try:
        app.iconbitmap("resources/images/logo(ico).ico")
    except Exception as e:
        print("[Icon Error]", e)

    current_view = None
    active_button = None
    button_refs = {}

    logo_img = None
    try:
        logo_path = "resources/images/logo.png"
        if os.path.exists(logo_path):
            logo_img = ctk.CTkImage(Image.open(logo_path), size=(32, 32))
    except Exception as e:
        print("[Logo PNG Error]", e)

    appearance = ctk.get_appearance_mode()
    sidebar_color = "#1f2937" if appearance == "Dark" else None

    sidebar = ctk.CTkFrame(app, width=220, corner_radius=0, fg_color=sidebar_color)
    sidebar.pack(side="left", fill="y")

    logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    logo_frame.pack(pady=(15, 10))
    if logo_img:
        ctk.CTkLabel(logo_frame, image=logo_img, text="").pack(side="left", padx=(5, 8))
    ctk.CTkLabel(logo_frame, text="T3K Cleaner", font=("Segoe UI", 16, "bold")).pack(side="left")

    section_system_var = tk.StringVar(value="— " + tr("section_system") + " —")
    section_info_var = tk.StringVar(value="— " + tr("section_info") + " —")
    sysinfo_title_var = tk.StringVar(value=tr("sysinfo_title"))

    def section_title(var):
        return ctk.CTkLabel(sidebar, textvariable=var, font=("Segoe UI", 12, "bold"), text_color="#aaa")

    section_title(section_system_var).pack(anchor="w", padx=15, pady=(10, 0))

    def create_sidebar_button(label_var, key):
        btn = ctk.CTkButton(
            sidebar, textvariable=label_var, font=("Segoe UI", 14), anchor="w",
            fg_color="transparent", hover_color=PRIMARY_COLOR, corner_radius=8,
            command=lambda k=key: switch_view(k)
        )
        btn.bind("<Enter>", lambda e, b=btn: b.configure(fg_color=PRIMARY_COLOR) if b != active_button else None)
        btn.bind("<Leave>", lambda e, b=btn: b.configure(fg_color="transparent") if b != active_button else None)
        btn.pack(fill="x", padx=12, pady=4)
        button_refs[key] = btn

    create_sidebar_button(labels["home"], "home")
    create_sidebar_button(labels["scan"], "scan")
    create_sidebar_button(labels["clean"], "clean")
    create_sidebar_button(labels["settings"], "settings")

    section_title(section_info_var).pack(anchor="w", padx=15, pady=(15, 0))
    create_sidebar_button(labels["history"], "history")

    ctk.CTkButton(
        sidebar, textvariable=labels["exit"], font=("Segoe UI", 14), anchor="w",
        fg_color="#ef4444", hover_color="#dc2626", corner_radius=8,
        command=app.destroy
    ).pack(fill="x", padx=12, pady=(20, 5))

    main_wrapper = ctk.CTkFrame(app)
    main_wrapper.pack(side="left", fill="both", expand=True)

    main_content = ctk.CTkFrame(main_wrapper, corner_radius=0)
    main_content.pack(side="left", fill="both", expand=True)

    sysinfo_panel = ctk.CTkFrame(main_wrapper, width=220)
    sysinfo_panel.pack(side="right", fill="y", padx=(0, 10), pady=10)

    sysinfo_title = ctk.CTkLabel(sysinfo_panel, textvariable=sysinfo_title_var, font=("Segoe UI", 14, "bold"))
    sysinfo_title.pack(pady=(10, 20))

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
        for widget in sysinfo_panel.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget != sysinfo_title:
                widget.destroy()
        for line in info:
            ctk.CTkLabel(sysinfo_panel, text=line, font=("Segoe UI", 12)).pack(pady=2, anchor="w", padx=10)

    def switch_view(name):
        nonlocal current_view
        for frame in views.values():
            frame.pack_forget()
        views[name].pack(fill="both", expand=True)
        update_sysinfo()
        set_active(button_refs[name])

    views = {
        "home": build_home_view(main_content, switch_view),
        "scan": build_scan_view(main_content),
        "clean": build_clean_view(main_content),
        "history": build_history_view(main_content),
        "settings": build_settings_view(main_content),
    }

    def set_active(btn):
        nonlocal active_button
        if active_button:
            active_button.configure(fg_color="transparent")
        btn.configure(fg_color=PRIMARY_COLOR)
        active_button = btn

    def update_sidebar_texts():
        section_system_var.set("— " + tr("section_system") + " —")
        section_info_var.set("— " + tr("section_info") + " —")
        sysinfo_title_var.set(tr("sysinfo_title"))

    on_language_change(update_sidebar_texts)

    switch_view("home")
    set_active(button_refs["home"])

    app.mainloop()

def show_splash_screen():
    splash = ctk.CTk()
    splash.geometry("300x200")
    splash.title("T3K Cleaner")
    splash.overrideredirect(True)
    splash.eval('tk::PlaceWindow . center')

    frame = ctk.CTkFrame(splash, corner_radius=12)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    try:
        logo = ctk.CTkImage(Image.open("resources/images/logo.png"), size=(80, 80))
        ctk.CTkLabel(frame, image=logo, text="").pack(pady=(15, 10))
    except:
        pass

    loading_label = ctk.CTkLabel(frame, text="Đang khởi động", font=("Segoe UI", 14))
    loading_label.pack(pady=(10, 5))

    def animate_dots(i=0):
        dots = ["", ".", "..", "..."]
        loading_label.configure(text=f"Đang khởi động{dots[i % 4]}")
        if i < 6:
            splash.after(500, animate_dots, i + 1)
        else:
            splash.destroy()
            main_app()

    animate_dots()
    splash.mainloop()

if __name__ == "__main__":
    show_splash_screen()
