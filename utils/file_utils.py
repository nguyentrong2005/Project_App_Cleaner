import os
import tempfile
from pathlib import Path


def can_delete(path: Path) -> bool:
    """
    Kiểm tra xem có quyền ghi vào file/thư mục hay không.
    Trả về True nếu có thể xóa.
    """
    return os.access(path, os.W_OK)


def is_file_locked(path: Path) -> bool:
    """
    Kiểm tra file có bị khóa (đang được sử dụng bởi chương trình khác) hay không.
    Cách làm: thử mở file với quyền ghi.
    Nếu mở không được → file đang bị khóa.
    """
    if not path.is_file():
        return False

    try:
        with open(path, 'a'):
            return False  # Mở được → không bị khóa
    except (PermissionError, OSError):
        return True  # Không mở được → bị khóa hoặc lỗi khác


def check_permissions(path: Path) -> dict:
    """
    Trả về dict các quyền trên path:
    - read: có thể đọc
    - write: có thể ghi
    - execute: có thể thực thi
    - delete: có thể xóa (cần quyền ghi lên thư mục cha)
    """
    permissions = {
        "read": os.access(path, os.R_OK),
        "write": os.access(path, os.W_OK),
        "execute": os.access(path, os.X_OK),
    }

    try:
        permissions["delete"] = os.access(path.parent, os.W_OK)
    except Exception:
        permissions["delete"] = False

    return permissions