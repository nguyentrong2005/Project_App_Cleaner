# gui_helpers.py
"""
Module hỗ trợ giao diện người dùng cho CleanerApp.

Chức năng:
- Hiển thị popup chi tiết danh sách file (ví dụ khi double-click loại rác)
- Có khả năng phân trang (mỗi lần hiển thị thêm 100 mục)
"""

import customtkinter as ctk
import tkinter as tk
import random
from gui.localization import tr


def show_detail_popup(title: str, files: list[str]) -> None:
    """
    Hiển thị một popup với danh sách file chi tiết (dùng trong phần quét rác).

    - Danh sách sẽ hiển thị theo từng nhóm 100 mục.
    - Mỗi hàng gồm: đường dẫn + dung lượng mô phỏng (random).
    - Có nút "Xem thêm" để hiển thị thêm dữ liệu.

    Args:
        title (str): Tiêu đề của popup.
        files (list[str]): Danh sách các đường dẫn file.
    """
    popup = ctk.CTkToplevel()
    popup.title(title)
    popup.geometry("600x400")
    popup.attributes("-topmost", True)

    # Căn giữa popup trên màn hình
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() - 600) // 2
    y = (popup.winfo_screenheight() - 400) // 2
    popup.geometry(f"+{x}+{y}")

    # Tiêu đề chính
    ctk.CTkLabel(popup, text=title, font=(
        "Segoe UI", 16, "bold")).pack(pady=10)

    # Header cho danh sách: Đường dẫn | Dung lượng
    header = ctk.CTkFrame(popup, fg_color="transparent")
    header.pack(fill="x", padx=10, pady=(0, 5))
    ctk.CTkLabel(header, text=tr("detail_col_path"), anchor="w").pack(
        side="left", fill="x", expand=True)
    ctk.CTkLabel(header, text=tr("detail_col_size"),
                 width=100, anchor="e").pack(side="right")

    # Vùng hiển thị danh sách
    list_frame = ctk.CTkScrollableFrame(popup)
    list_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Nút "Xem thêm"
    show_more_btn = ctk.CTkButton(popup, text=tr("show_more"))
    show_more_btn.configure(command=lambda: render_more())

    # Biến đếm số lượng đã hiển thị
    displayed_count = tk.IntVar(value=0)
    total_files = len(files)
    step = 100  # Số lượng file mỗi lần "Xem thêm"

    def render_more():
        """
        Hiển thị thêm các dòng file tiếp theo (tối đa 100 mỗi lần).
        Ẩn nút "Xem thêm" khi đã hiển thị hết.
        """
        start = displayed_count.get()
        end = min(start + step, total_files)

        for fpath in files[start:end]:
            # Mô phỏng dung lượng file (để test hiển thị)
            size = round(random.uniform(10, 500), 2)

            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=1)

            ctk.CTkLabel(row, text=fpath, anchor="w").pack(
                side="left", fill="x", expand=True)
            ctk.CTkLabel(row, text=f"{size} KB",
                         width=100, anchor="e").pack(side="right")

        displayed_count.set(end)

        # Kiểm tra còn dữ liệu không
        if displayed_count.get() >= total_files:
            show_more_btn.pack_forget()
        else:
            show_more_btn.pack(pady=(0, 10))

    # Gọi lần đầu để hiển thị 100 mục đầu tiên
    render_more()
