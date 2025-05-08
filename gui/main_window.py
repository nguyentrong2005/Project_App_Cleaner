import tkinter as tk
from tkinter import messagebox, ttk

class CleanerAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CleanerApp - By Trongdepzai")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # ======== Buttons ========
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.scan_btn = tk.Button(button_frame, text="Quét", width=10, command=self.scan_action)
        self.scan_btn.pack(side=tk.LEFT, padx=10)

        self.clean_btn = tk.Button(button_frame, text="Dọn", width=10, command=self.clean_action)
        self.clean_btn.pack(side=tk.LEFT, padx=10)

        self.exit_btn = tk.Button(button_frame, text="Thoát", width=10, command=self.root.quit)
        self.exit_btn.pack(side=tk.LEFT, padx=10)

        # ======== File List Display ========
        self.result_box = tk.Text(self.root, height=15, width=70)
        self.result_box.pack(pady=10)
        self.result_box.insert(tk.END, "Danh sách file rác sẽ hiển thị ở đây...\n")

        # ======== Status Bar ========
        self.status = tk.StringVar()
        self.status.set("Trạng thái: Sẵn sàng")
        self.status_bar = tk.Label(self.root, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def scan_action(self):
        self.result_box.insert(tk.END, "\nĐang quét file rác...\n")
        self.status.set("Trạng thái: Đang quét...")

    def clean_action(self):
        self.result_box.insert(tk.END, "\nDọn rác hoàn tất!\n")
        self.status.set("Trạng thái: Đã dọn rác")

# Chạy app
if __name__ == "__main__":
    root = tk.Tk()
    app = CleanerAppGUI(root)
    root.mainloop()