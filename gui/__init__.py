"""
Gói `gui` của CleanerApp.

Chứa toàn bộ thành phần giao diện người dùng, xây dựng bằng CustomTkinter:
- home_view: Trang chủ
- scan_view: Quét hệ thống
- clean_view: Dọn rác
- history_view: Lịch sử dọn dẹp
- settings_view: Cài đặt (giao diện, ngôn ngữ)
- sidebar_labels: Quản lý nhãn của sidebar (StringVar + tự cập nhật khi đổi ngôn ngữ)
- localization: Hệ thống đa ngôn ngữ (i18n)
- main_window: Giao diện chính và splash screen
"""

from .home_view import build_home_view
from .scan_view import build_scan_view

from .history_view import build_history_view
from .settings_view import build_settings_view
from .sidebar_labels import init_sidebar_labels
from .localization import tr, set_language, on_language_change
from .main_window import run_main_window