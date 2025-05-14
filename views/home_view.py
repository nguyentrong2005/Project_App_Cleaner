import customtkinter as ctk

PRIMARY_COLOR = "#3b82f6"
HOVER_BG = "#2a2e35"  # nền khi hover

def build_home_view(main_content):
    home = ctk.CTkFrame(main_content)

    # Tiêu đề chính
    ctk.CTkLabel(
        home,
        text="🧹 Chào mừng đến với App Cleaner",
        font=("Segoe UI", 24, "bold"),
        anchor="center",
        justify="center"
    ).pack(pady=(40, 10))

    # Mô tả nhỏ
    ctk.CTkLabel(
        home,
        text="Loại bỏ rác hệ thống để giải phóng dung lượng và tăng hiệu suất máy.",
        font=("Segoe UI", 14),
        justify="center"
    ).pack(pady=(0, 30))

    # Card dọn rác
    card = ctk.CTkFrame(home, corner_radius=12, border_width=2, border_color=PRIMARY_COLOR, height=150)
    card.pack(padx=80, pady=10, fill="x")

    row = ctk.CTkFrame(card, fg_color="transparent")
    row.pack(expand=True, fill="both", padx=20, pady=20)

    icon_label = ctk.CTkLabel(row, text="🧹", font=("Segoe UI", 48), width=80)
    icon_label.pack(side="left")

    text_label = ctk.CTkLabel(row, text="Dọn rác hệ thống", font=("Segoe UI", 20, "bold"))
    text_label.pack(side="left", padx=20)

    # Hover effect
    def on_enter(e):
        card.configure(border_color="#60a5fa", fg_color=HOVER_BG)

    def on_leave(e):
        card.configure(border_color=PRIMARY_COLOR, fg_color="transparent")

    for widget in [card, row, icon_label, text_label]:
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    # Click để chuyển sang clean view
    def open_clean_view(event=None):
        for child in home.winfo_toplevel().winfo_children():
            if isinstance(child, ctk.CTkFrame):
                for btn in child.winfo_children():
                    if isinstance(btn, ctk.CTkButton) and "Dọn" in btn.cget("text"):
                        btn.invoke()
                        return

    for widget in [card, row, icon_label, text_label]:
        widget.bind("<Button-1>", open_clean_view)

    # Mẹo nhỏ
    ctk.CTkLabel(
        home,
        text="💡 Mẹo: Dọn rác định kỳ giúp máy hoạt động ổn định và nhanh hơn.",
        font=("Segoe UI", 12),
        text_color="#aaa"
    ).pack(pady=30)

    return home
