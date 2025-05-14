import os
import tempfile
from pathlib import Path


def can_delete(path: Path) -> bool:
    """
    Kiểm tra xem có quyền ghi và xóa file/thư mục hay không.
    Trả về True nếu có quyền.
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


# ✅ Chạy thử để test 2 hàm tiện ích
if __name__ == "__main__":
    test_file = Path(tempfile.gettempdir()) / "test_temp_file.txt"
    test_file.touch(exist_ok=True)

    print(f"File: {test_file}")
    print("Có thể xóa:", can_delete(test_file))
    print("Có bị khóa:", is_file_locked(test_file))

    test_file.unlink(missing_ok=True)
