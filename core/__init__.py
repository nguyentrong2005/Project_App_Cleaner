"""
Module `core` của CleanerApp.

Chứa các thành phần cốt lõi xử lý logic chính:
- TrashScanner: Quét hệ thống để tìm file/thư mục rác
- scan_and_log: Hàm điều phối toàn bộ quá trình quét, thời gian quét và ghi log
- rules: Tập hợp các luật xác định rác, vùng quét, điều kiện an toàn, phân quyền xóa
- get_system_info: Lấy thông tin hệ thống thật (OS, CPU, RAM, ổ đĩa, pin)

Đây là module trung tâm liên kết giữa chức năng nhận diện rác, hiển thị thông tin hệ thống và ghi kết quả.
"""

from .scanner import TrashScanner, scan_and_log
from .rules import (
    get_scan_directories,
    is_safe_path,
    is_garbage_file,
    is_empty_directory,
    can_delete,
    get_grouping_root
)
from .system_info import get_system_info
