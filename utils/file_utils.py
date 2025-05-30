"""
Module `file_utils` - hỗ trợ thao tác hệ thống file cho CleanerApp.

Chức năng chính:
- Kiểm tra file có bị khóa hay không (đang được chương trình khác sử dụng)
- Kiểm tra các quyền truy cập trên file/thư mục (đọc, ghi, xóa, thực thi)
"""

import os
from pathlib import Path


def is_file_locked(path: Path) -> bool:
    """
    Kiểm tra một file có bị khóa hay không (đang được sử dụng bởi chương trình khác).

    Args:
        path (Path): Đường dẫn tới file cần kiểm tra.

    Returns:
        bool: True nếu file bị khóa hoặc không thể mở ghi,
              False nếu có thể truy cập ghi (không bị khóa).
    """
    if not path.is_file():
        return False

    try:
        with open(path, 'a'):
            return False
    except (PermissionError, OSError):
        return True


def check_permissions(path: Path) -> dict:
    """
    Kiểm tra các quyền truy cập trên file hoặc thư mục.

    Args:
        path (Path): Đường dẫn đến file hoặc thư mục.

    Returns:
        dict: Dictionary chứa các quyền:
            - read (bool): có thể đọc
            - write (bool): có thể ghi
            - execute (bool): có thể thực thi
            - delete (bool): có thể xóa (dựa vào quyền ghi thư mục cha)
    """
    return {
        "read": os.access(path, os.R_OK),
        "write": os.access(path, os.W_OK),
        "execute": os.access(path, os.X_OK),
        "delete": os.access(path.parent, os.W_OK) if path.parent.exists() else False
    }
