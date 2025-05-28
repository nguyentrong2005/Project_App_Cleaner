import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time
import threading
import random
from .localization import tr, on_language_change
from controller.app_controller import scan_and_return_summary
from controller.app_controller import delete_selected_files


TRASH_TYPES = [
    "Internet Cache", "Cookies", "Internet History", "Metrics Temp File",
    "Temporary Internet Files", "Thumbnail Cache", "Empty Recycle Bin",
    "Temporary Files", "Memory Dumps", "Windows Log Files",
    "Windows Web Cache", "Microsoft OneDrive"
]


def generate_fake_data():
    data = {}
    for cat in TRASH_TYPES:
        count = random.randint(5, 50)
        size = round(random.uniform(1, 100), 2)
        files = [
            f"C:/Fake/{cat.replace(' ', '_')}/file_{i}.tmp" for i in range(count)]
        data[cat] = {"count": count, "size": size, "files": files}
    return data


def build_scan_view(main_content, refresh_history=None):
    f = ctk.CTkFrame(main_content)
    file_vars = {}
    selected_files = []
    state = {"view": "main"}
    all_data = {}

    # Ngôn ngữ động
    clean_btn_text = tk.StringVar(value=tr("scan_clean"))
    scan_btn_text = tk.StringVar(value=tr("scan_start"))
    back_btn_text = tk.StringVar(value=tr("scan_back"))
    progress_text = tk.StringVar(value=tr("scan_progress"))
    title_var = tk.StringVar(value=tr("scan_title"))
    desc_var = tk.StringVar(value=tr("scan_desc"))
    col_size_var = tk.StringVar(value=tr("scan_col_size"))
    col_count_var = tk.StringVar(value=tr("scan_col_count"))
    col_path_var = tk.StringVar(value=tr("detail_col_path"))
    col_size_var = tk.StringVar(value=tr("detail_col_size"))
    time_var = tk.StringVar(value="⏱ 0.0s")

    # Tiêu đề
    ctk.CTkLabel(f, textvariable=title_var, font=(
        "Segoe UI", 22, "bold")).pack(pady=(20, 10))
    ctk.CTkLabel(f, textvariable=desc_var, font=(
        "Segoe UI", 14)).pack(pady=(0, 20))

    # Tiến trình và thời gian
    progress_label = ctk.CTkLabel(
        f, textvariable=progress_text, font=("Segoe UI", 13))
    progress_label.pack()

    ctk.CTkLabel(f, textvariable=time_var, font=(
        "Segoe UI", 12), text_color="#aaa").pack()
    progress_bar = ctk.CTkProgressBar(f, width=500)
    progress_bar.set(0)
    progress_bar.pack(pady=(10, 20))

    # Bảng chính
    table_frame = ctk.CTkScrollableFrame(f, height=260)
    table_frame.pack(padx=20, pady=10, fill="x")

    back_btn = ctk.CTkButton(f, textvariable=back_btn_text,
                             command=lambda: show_main_view(), fg_color="#6b7280")
    back_btn.pack(pady=5)
    back_btn.pack_forget()

    clean_btn = ctk.CTkButton(f, textvariable=clean_btn_text,
                              command=lambda: start_cleanup(), fg_color="#10b981")
    clean_btn.pack(pady=10)
    clean_btn.pack_forget()

    def start_scan():
        scan_btn.configure(state="disabled")
        clean_btn.pack_forget()
        back_btn.pack_forget()
        for widget in table_frame.winfo_children():
            widget.destroy()
        progress_text.set(tr("scan_progress"))
        progress_bar.set(0)
        time_var.set("⏱ 0.0s")

        start_time = time.time()
        state["view"] = "scanning"

        def update_timer():
            if state["view"] != "scanning":
                return
            elapsed = time.time() - start_time
            time_var.set(f"⏱ {elapsed:.1f}s")

            # Tiến trình ước lượng dựa trên thời gian scan thực tế
            # Để tránh bị đầy quá sớm, bạn có thể dùng công thức mềm hơn:
            estimated_max_duration = 20  # bạn có thể điều chỉnh (ví dụ 10s)
            progress = min(elapsed / estimated_max_duration, 0.99)
            progress_bar.set(progress)

            f.after(100, update_timer)

        def run_scan():
            summary, classified_paths, total_size, duration = scan_and_return_summary()
            state["view"] = "main"
            f.after(0, lambda: on_scan_complete(
                summary, classified_paths, total_size, duration))

        def on_scan_complete(summary, classified_paths, total_size, duration):
            state["view"] = "main"
            progress_bar.set(1.0)
            progress_text.set(tr("scan_done"))
            time_var.set(f"⏱ {duration:.1f}s")
            show_main_view(summary, classified_paths, total_size, duration)
            if refresh_history:
                refresh_history()

        threading.Thread(target=run_scan, daemon=True).start()
        update_timer()  # ✅ gọi hàm cập nhật thời gian thật

    scan_btn = ctk.CTkButton(f, textvariable=scan_btn_text, command=start_scan)
    scan_btn.pack(pady=10)

    def show_main_view(summary=None, classified_paths=None, total_size=None, duration=None):
        state["view"] = "main"
        for widget in table_frame.winfo_children():
            widget.destroy()
        back_btn.pack_forget()
        clean_btn.pack(pady=10)
        scan_btn.configure(state="normal")

        nonlocal all_data
        if summary is None:
            summary, classified_paths, total_size, duration = scan_and_return_summary()
        all_data.clear()
        for rtype, (count, size) in summary.items():
            files = [str(p) for p in classified_paths[rtype]]
            all_data[rtype] = {
                "count": count,
                "size": round(size / 1024 / 1024, 2),  # MB
                "files": files
            }

       # ===== Header =====
        header = ctk.CTkFrame(table_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 5))

        select_all_var = tk.BooleanVar()

        def toggle_all():
            for var in file_vars.values():
                var.set(select_all_var.get())

        col_size_var = tk.StringVar(value=tr("scan_col_size"))
        col_count_var = tk.StringVar(value=tr("scan_col_count"))

        # Checkbox + tiêu đề “Loại rác”
        cb = ctk.CTkCheckBox(header, text=tr("scan_select_all"), variable=select_all_var,
                             command=toggle_all)
        cb.pack(side="left", padx=(5, 5), fill="x", expand=True)

        # Dung lượng + Số lượng
        ctk.CTkLabel(header, textvariable=col_size_var, width=120,
                     anchor="e").pack(side="left", padx=5)
        ctk.CTkLabel(header, textvariable=col_count_var,
                     width=100, anchor="e").pack(side="left", padx=5)

        # ===== Các dòng loại file =====
        for cat, data in all_data.items():
            row = ctk.CTkFrame(table_frame)
            row.pack(fill="x", pady=2)

            var = tk.BooleanVar()
            file_vars[cat] = var

        # CheckBox (không bind click)
            cb = ctk.CTkCheckBox(row, variable=var, text="", width=30)
            cb.pack(side="left", padx=(5, 0))

        # Khung để gom phần còn lại và bind double-click
            detail_frame = ctk.CTkFrame(row, fg_color="transparent")
            detail_frame.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(detail_frame, text=cat, anchor="w").pack(
                side="left", padx=5, fill="x", expand=True)
            ctk.CTkLabel(detail_frame, text=f"{data['size']} MB", width=120, anchor="e").pack(
                side="left", padx=5)
            ctk.CTkLabel(detail_frame, text=f"{data['count']} files", width=100, anchor="e").pack(
                side="left", padx=5)

            def open_detail(e, c=cat):
                show_detail_view(c, all_data[c]["files"])

            detail_frame.bind("<Double-Button-1>", open_detail)
            for w in detail_frame.winfo_children():
                w.bind("<Double-Button-1>", open_detail)

    def show_detail_view(category, files):
        state["view"] = "detail"
        back_btn.pack(pady=5)
        clean_btn.pack_forget()
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Tiêu đề loại rác
        title = ctk.CTkLabel(
            table_frame, text=f"📂 {category}", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="w", padx=10, pady=(5, 0))

        # Header cho danh sách file
        header = ctk.CTkFrame(table_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 2))
        ctk.CTkLabel(header, textvariable=col_path_var, anchor="w").pack(
            side="left", fill="x", expand=True)
        ctk.CTkLabel(header, textvariable=col_size_var,
                     width=100, anchor="e").pack(side="right")

        # Dữ liệu giả lập kích thước file
        for fpath in files:
            size = round(random.uniform(10, 500), 2)  # Kích thước giả lập (KB)

            row = ctk.CTkFrame(table_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=1)

            ctk.CTkLabel(row, text=fpath, anchor="w").pack(
                side="left", fill="x", expand=True)
            ctk.CTkLabel(row, text=f"{size} KB",
                         width=100, anchor="e").pack(side="right")

    def start_cleanup():
        selected = []
        for cat, var in file_vars.items():
            if var.get():
                selected.extend(all_data[cat]["files"])

        if not selected:
            messagebox.showwarning("⚠️", tr("scan_no_selection"))
            return

        confirm = messagebox.askyesno("Xác nhận", tr(
            "scan_confirm_delete").format(n=len(selected)))
        if not confirm:
            return

        progress_text.set("🧹 " + tr("scan_clean"))

        def run():
            deleted, failed = delete_selected_files(selected)

            for i in range(100, -1, -2):
                progress_text.set(f"🧹 {tr('scan_clean')}: {i}%")
                progress_bar.set(i / 100)
                time.sleep(0.02)

            message = tr("scan_deleted").format(n=len(deleted))
            if failed:
                message += f"\n⚠️ {len(failed)} mục không xóa được."

            progress_text.set(message)

        threading.Thread(target=run, daemon=True).start()

    def update_texts():
        clean_btn_text.set(tr("scan_clean"))
        scan_btn_text.set(tr("scan_start"))
        back_btn_text.set(tr("scan_back"))
        progress_text.set(tr("scan_progress"))
        title_var.set(tr("scan_title"))
        desc_var.set(tr("scan_desc"))
        col_size_var.set(tr("scan_col_size"))
        col_count_var.set(tr("scan_col_count"))
        col_path_var.set(tr("detail_col_path"))
        col_size_var.set(tr("detail_col_size"))

    on_language_change(update_texts)

    return f
