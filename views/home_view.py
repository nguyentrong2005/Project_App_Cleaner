import customtkinter as ctk

def build_home_view(main_content):
    home = ctk.CTkFrame(main_content)

    ctk.CTkLabel(
        home,
        text="📊 Tình trạng hệ thống",
        font=("Segoe UI", 22, "bold"),
        anchor="center"
    ).pack(pady=(20, 10))

    ctk.CTkLabel(
        home,
        text="Đã phát hiện 1015 tập tin không cần thiết (932 MB)\nHãy tối ưu hoá hệ thống của bạn!",
        font=("Segoe UI", 14),
        justify="center"
    ).pack(pady=(0, 20))

    container = ctk.CTkFrame(home)
    container.pack(padx=30, pady=10, fill="both", expand=True)

    labels = [
        ("🌐", "Dấu vết trình duyệt"),
        ("🧾", "Registry lỗi"),
        ("🔗", "Shortcut không hợp lệ"),
        ("⚙️", "Dịch vụ đang chạy"),
        ("🚀", "Tác vụ khởi động"),
        ("🔧", "Tuỳ chỉnh hệ thống"),
    ]

    for i, (icon, text) in enumerate(labels):
        card = ctk.CTkFrame(container, corner_radius=12, border_width=1, height=80)
        card.grid(row=i//2, column=i%2, padx=20, pady=15, sticky="nsew")

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="both", expand=True, padx=10, pady=10)

        icon_label = ctk.CTkLabel(row, text=icon, font=("Segoe UI", 24), width=40)
        icon_label.pack(side="left")

        text_label = ctk.CTkLabel(row, text=text, font=("Segoe UI", 14))
        text_label.pack(side="left", padx=10)

    container.grid_columnconfigure((0, 1), weight=1)
    container.grid_rowconfigure((0, 1, 2), weight=1)

    btn_frame = ctk.CTkFrame(home, fg_color="transparent")
    btn_frame.pack(pady=20)

    ctk.CTkButton(btn_frame, text="🔄 Phân tích lại", width=140, fg_color="#3b82f6").pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="⚡ Tối ưu hoá", width=140, fg_color="#10b981").pack(side="left", padx=10)

    return home
