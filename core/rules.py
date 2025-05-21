import os
from pathlib import Path
import tempfile
from utils import check_permissions

GARBAGE_EXTENSIONS = ['.tmp', '.log', '.bak',
                      '.old', '.temp', '.chk', '.~', '.dmp', '.cache']


def get_scan_directories() -> list[Path]:
    """
    Trả về danh sách các thư mục hệ thống có khả năng chứa file rác.
    Gồm: %TEMP%, AppData\Local, AppData\Roaming, Downloads,...
    """
    home = Path.home()
    return [
        Path(tempfile.gettempdir()),                        # %TEMP% hiện tại
        Path('C:/Windows/Temp'),                            # TEMP hệ thống
        home / 'Downloads',                                 # Tải về
        home / 'AppData' / 'Local' / 'Temp',                # AppData Temp
        home / 'AppData' / 'Local',                         # AppData Local
        home / 'AppData' / 'Roaming',                       # AppData Roaming
    ]


DANGEROUS_FOLDERS = [
    Path("C:/Windows"),
    Path("C:/Program Files"),
    Path("C:/Program Files (x86)"),
    Path.home() / "Documents",
    Path.home() / "Pictures",
    Path.home() / "Videos",
    Path.home() / "Desktop"
]


def is_safe_path(path: Path) -> bool:
    """
    Kiểm tra xem path có nằm trong danh sách vùng nguy hiểm không.
    Trả về False nếu nằm trong thư mục hệ thống quan trọng (Windows, Program Files, Documents,...).
    """
    for danger in DANGEROUS_FOLDERS:
        try:
            if str(path).lower().startswith(str(danger).lower()):
                return False
        except Exception:
            continue
    return True


def is_garbage_file(file_path: Path) -> bool:
    """
    Kiểm tra xem một file có được coi là rác không.
    Một file được coi là rác nếu:
    - Có phần mở rộng trong danh sách GARBAGE_EXTENSIONS
    - Hoặc có kích thước bằng 0 byte
    """
    try:
        if not file_path.exists() or not file_path.is_file():
            return False
        if file_path.suffix.lower() in GARBAGE_EXTENSIONS:
            return True
        if file_path.stat().st_size == 0:
            return True
    except Exception:
        pass
    return False


def is_empty_directory(dir_path: Path) -> bool:
    """
    Kiểm tra xem thư mục có hoàn toàn rỗng không.
    Trả về True nếu không có file hoặc thư mục con nào.
    """
    try:
        return dir_path.exists() and dir_path.is_dir() and not any(dir_path.iterdir())
    except (PermissionError, OSError):
        return False


def is_writable(path: Path) -> bool:
    """
    Kiểm tra quyền ghi (write) trên path (file hoặc thư mục).
    Trả về True nếu có quyền ghi.
    """
    return os.access(path, os.W_OK)


def can_delete(path: Path) -> bool:
    """
    Kiểm tra xem path có thể bị xóa không.
    Dựa trên:
    - Quyền ghi lên path
    - Quyền ghi lên thư mục cha (để thực hiện xóa)
    """
    perms = check_permissions(path)
    return perms["delete"] and perms["write"]


def get_grouping_root(path: Path) -> Path:
    """
    Trả về thư mục gốc cấp cao trong danh sách quét mà path thuộc về.
    Dùng để gom nhóm các file rác khi ghi log.
    Nếu không tìm thấy thư mục gốc phù hợp, trả về path cha gần nhất.
    """
    roots = get_scan_directories()
    for root in roots:
        try:
            if root in path.parents:
                return root
        except Exception:
            continue
    return path.parent
