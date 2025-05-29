"""
Module `core` của CleanerApp.

Chứa các thành phần cốt lõi xử lý logic chính:
- TrashScanner: Quét hệ thống để tìm file/thư mục rác
- TrashCleaner: Xóa các file/thư mục rác đã quét
- run_scan: Hàm dùng để quét rác và xuất kết quả
- Các hàm lưu lịch sử dọn rác
- rules: Các quy tắc xác định loại rác, phân quyền và vùng quét
- get_system_info: Lấy thông tin hệ thống thật (OS, CPU, RAM, ổ đĩa, pin)

Đây là module trung tâm liên kết giữa:
- chức năng nhận diện và phân loại rác,
- xử lý quét, xóa,
- và hiển thị kết quả/hệ thống.
"""

from .scanner import TrashScanner, run_scan
from .cleaner import TrashCleaner, save_clean_summary_log, save_clean_per_type_detail
from .rules import (
    get_scan_directories,
    is_safe_path,
    is_garbage_file,
    is_empty_directory,
    can_delete,
    get_grouping_root,
    detect_installed_browsers,
    get_garbage_type,
    GARBAGE_TYPES
)
from .system_info import get_system_info

__all__ = [
    # scanner
    "TrashScanner", "run_scan",
    # cleaner
    "TrashCleaner", "save_clean_summary_log", "save_clean_per_type_detail",
    # rules
    "get_scan_directories", "is_safe_path", "is_garbage_file", "is_empty_directory",
    "can_delete", "get_grouping_root", "detect_installed_browsers",
    "get_garbage_type", "GARBAGE_TYPES",
    # system info
    "get_system_info"
]
