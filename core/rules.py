import os
from pathlib import Path

# Danh sách phần mở rộng file được coi là rác
EXTENSIONS = ['.tmp', '.log', '.bak']

def is_garbage_file(file_path: Path) -> bool:
    """
    Kiểm tra file có phải là rác không:
    - Có đuôi trong EXTENSIONS
    - Hoặc có dung lượng = 0 byte
    """
    if file_path.suffix.lower() in EXTENSIONS:
        return True
    if file_path.stat().st_size == 0:
        return True
    return False

def is_empty_directory(dir_path: Path) -> bool:
    """
    Kiểm tra xem thư mục có rỗng hoàn toàn không
    """
    return dir_path.exists() and dir_path.is_dir() and not any(dir_path.iterdir())

def is_writable(path: Path) -> bool:
    """
    Kiểm tra có quyền ghi vào file/thư mục để đảm bảo có thể xóa
    """
    return os.access(path, os.W_OK)
