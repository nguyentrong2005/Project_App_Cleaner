import customtkinter as ctk

def build_history_view(main_content):
    f = ctk.CTkFrame(main_content)

    ctk.CTkLabel(f, text="📜 Lịch sử dọn dẹp", font=("Segoe UI", 22, "bold")).pack(pady=(20, 10))
    ctk.CTkLabel(f, text="Dưới đây là các lần dọn hệ thống gần nhất:", font=("Segoe UI", 14)).pack(pady=(0, 10))

    table = ctk.CTkScrollableFrame(f, height=250)
    table.pack(padx=20, pady=10, fill="x")

    headers = ("🕒 Thời gian", "🧹 Số mục", "💾 Dung lượng")
    header_text = f"{headers[0]:<25}{headers[1]:<15}{headers[2]}"
    ctk.CTkLabel(table, text=header_text, font=("Segoe UI", 13, "bold"), text_color="#3b82f6").pack(anchor="w", padx=(10,20), pady=(5, 8))

    history = [
        ("2025-05-07 14:32", "5 mục", "420 MB"),
        ("2025-05-06 11:20", "8 mục", "932 MB"),
        ("2025-05-01 09:02", "6 mục", "750 MB"),
    ]
    for time_str, items, size in history:
        line = f"{time_str:<25}{items:<15}{size}"
        ctk.CTkLabel(table, text=line, font=("Segoe UI", 13)).pack(anchor="w", padx=20, pady=3)

    return f
