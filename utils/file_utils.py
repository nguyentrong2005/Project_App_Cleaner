import os
from pathlib import Path


def is_file_locked(path: Path) -> bool:
    """
    Kiểm tra file có bị khóa (đang được sử dụng bởi chương trình khác) hay không.
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
    Trả về dict các quyền trên path:
    - read: có thể đọc
    - write: có thể ghi
    - execute: có thể thực thi
    - delete: có thể xóa (cần quyền ghi thư mục cha)
    """
    return {
        "read": os.access(path, os.R_OK),
        "write": os.access(path, os.W_OK),
        "execute": os.access(path, os.X_OK),
        "delete": os.access(path.parent, os.W_OK) if path.parent.exists() else False
    }
