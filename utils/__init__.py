"""
Package `utils` của CleanerApp.

Chức năng:
- Các hàm kiểm tra trạng thái file: quyền truy cập, khóa sử dụng
- Hàm hỗ trợ gọi .after() an toàn trong Tkinter
- Popup helper: Hiển thị danh sách file chi tiết với khả năng phân trang

Modules:
- file_utils: is_file_locked, check_permissions
- safe_after: safe_after, safe_run
- gui_helpers: show_detail_popup
"""

from .file_utils import is_file_locked, check_permissions
from .safe_after import safe_after, safe_run
from .gui_helpers import show_detail_popup

__all__ = [
    # file_utils
    "is_file_locked", "check_permissions",
    # safe_after
    "safe_after", "safe_run",
    # gui_helpers
    "show_detail_popup"
]
