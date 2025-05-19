# sidebar_labels.py
import tkinter as tk
from gui.localization import tr, on_language_change

_labels = {}


def init_sidebar_labels():
    global _labels
    _labels = {
        "home": tk.StringVar(value="🏠 " + tr("home_label")),
        "scan": tk.StringVar(value="🔍 " + tr("scan_label")),
        "clean": tk.StringVar(value="🧹 " + tr("clean_label")),
        "settings": tk.StringVar(value="⚙️ " + tr("settings_label")),
        "history": tk.StringVar(value="📜 " + tr("history_label")),
        "exit": tk.StringVar(value="❌ " + tr("exit_label")),
    }

    def update():
        _labels["home"].set("🏠 " + tr("home_label"))
        _labels["scan"].set("🔍 " + tr("scan_label"))
        _labels["clean"].set("🧹 " + tr("clean_label"))
        _labels["settings"].set("⚙️ " + tr("settings_label"))
        _labels["history"].set("📜 " + tr("history_label"))
        _labels["exit"].set("❌ " + tr("exit_label"))

    on_language_change(update)
    return _labels  # ✅ trả về dict label đã tạo
