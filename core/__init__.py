"""
Module `core` của CleanerApp.

Chứa các thành phần cốt lõi xử lý logic chính:
- TrashScanner: Quét hệ thống để tìm file/thư mục rác
- TrashCleaner: Xóa các file/thư mục rác đã quét
- run_scan: Hàm dùng để quét rác và xuất kết quả
- run_clean: Hàm dùng để dọn rác và lưu lịch sử dọn
- rules: Các quy tắc xác định loại rác, phân quyền và vùng quét
- get_system_info: Lấy thông tin hệ thống thật (OS, CPU, RAM, ổ đĩa, pin)

Đây là module trung tâm liên kết giữa:
- chức năng nhận diện và phân loại rác,
- xử lý quét, xóa,
- và hiển thị kết quả/hệ thống.
"""

from .scanner import TrashScanner, run_scan
from .cleaner import TrashCleaner, run_clean
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
