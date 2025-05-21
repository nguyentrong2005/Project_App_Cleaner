# sidebar_labels.py
import tkinter as tk
from gui.localization import tr, on_language_change

_labels = {}  # Biến toàn cục lưu các StringVar cho sidebar


def init_sidebar_labels():
    """
    Khởi tạo các nhãn (label) hiển thị trong sidebar điều hướng của ứng dụng.

    - Mỗi mục sẽ là một `tk.StringVar` chứa icon + văn bản tương ứng
    - Nội dung được dịch tự động qua `tr()` (theo ngôn ngữ hiện tại)
    - Tự động cập nhật lại nội dung khi ngôn ngữ thay đổi (qua callback on_language_change)

    Labels được tạo:
        - home: Trang chủ
        - scan: Quét
        - clean: Dọn
        - settings: Cài đặt
        - history: Lịch sử
        - exit: Thoát

    Returns:
        dict[str, tk.StringVar]: Dictionary chứa các label của sidebar
    """
    global _labels
    _labels = {
        "home": tk.StringVar(value="🏠 " + tr("home_label")),
        "scan": tk.StringVar(value="🔍 " + tr("scan_label")),
        "settings": tk.StringVar(value="⚙️ " + tr("settings_label")),
        "history": tk.StringVar(value="📜 " + tr("history_label")),
        "exit": tk.StringVar(value="❌ " + tr("exit_label")),
    }

    def update():
        """
        Hàm nội bộ: Cập nhật lại toàn bộ label khi ngôn ngữ thay đổi.
        """
        _labels["home"].set("🏠 " + tr("home_label"))
        _labels["scan"].set("🔍 " + tr("scan_label"))
        _labels["settings"].set("⚙️ " + tr("settings_label"))
        _labels["history"].set("📜 " + tr("history_label"))
        _labels["exit"].set("❌ " + tr("exit_label"))

    on_language_change(update)
    return _labels
