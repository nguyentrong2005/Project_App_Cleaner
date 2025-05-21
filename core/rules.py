# rules.py
"""
Module chứa các quy tắc xử lý rác cho CleanerApp.

- Xác định các loại file/thư mục rác
- Xác định quyền xóa, an toàn hệ thống
- Phân loại rác theo 12 nhóm
- Xác định trình duyệt đã cài để phân tích cache
"""

import os
from pathlib import Path
import tempfile
from utils import check_permissions

GARBAGE_TYPES = [
    "Internet cache",
    "Cookies",
    "Internet history",
    "Metrics temp file",
    "Temporary internet files",
    "Thumbnail cache",
    "Empty recycle bin",
    "Temporary files",
    "Memory dumps",
    "Windows log files",
    "Windows web cache",
    "Microsoft OneDrive"
]

GARBAGE_EXTENSIONS = ['.tmp', '.log', '.bak',
                      '.old', '.temp', '.chk', '.~', '.dmp', '.cache']


def get_scan_directories() -> list[Path]:
    """
    Trả về danh sách thư mục cần quét rác, bao gồm các vị trí phổ biến trong hệ thống:
    - Temp
    - AppData
    - Logs
    - Trình duyệt
    - OneDrive
    """
    home = Path.home()
    return [
        Path(tempfile.gettempdir()),
        Path("C:/Windows/Temp"),
        Path("C:/Windows/Logs"),
        Path("C:/$Recycle.Bin"),
        home / "Downloads",
        home / "AppData" / "Local" / "Temp",
        home / "AppData" / "Local",
        home / "AppData" / "Roaming",
        home / "AppData" / "Local" / "Microsoft" / "Windows" / "WebCache",
        home / "AppData" / "Local" / "Microsoft" / "Windows" / "INetCache",
        home / "AppData" / "Local" / "Microsoft" / "Windows" / "Explorer",
        home / "AppData" / "Local" / "Google" / "Chrome" / "User Data",
        home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data",
        home / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "Profiles",
        home / "AppData" / "Local" / "Microsoft" / "OneDrive"
    ]


def is_safe_path(path: Path) -> bool:
    """
    Kiểm tra đường dẫn có nằm ngoài vùng nguy hiểm hay không (Windows, Program Files, Documents).
    Dùng để đảm bảo an toàn khi quét và xóa.
    """
    dangerous = [Path("C:/Windows"), Path("C:/Program Files"),
                 Path.home() / "Documents"]
    return not any(str(path).lower().startswith(str(d).lower()) for d in dangerous)


def is_garbage_file(file_path: Path) -> bool:
    """
    Xác định một file có phải rác hay không dựa trên:
    - Đuôi mở rộng nằm trong danh sách GARBAGE_EXTENSIONS
    - File có dung lượng bằng 0 byte
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
    Trả về True nếu thư mục tồn tại và hoàn toàn rỗng.
    """
    try:
        return dir_path.exists() and dir_path.is_dir() and not any(dir_path.iterdir())
    except:
        return False


def can_delete(path: Path) -> bool:
    """
    Kiểm tra xem có thể xóa path hay không dựa trên:
    - Quyền ghi
    - Quyền xóa thư mục cha
    """
    perms = check_permissions(path)
    return perms["delete"] and perms["write"]


def get_grouping_root(path: Path) -> Path:
    """
    Tìm thư mục gốc cấp cao nhất của path nằm trong vùng quét được cấu hình.
    Dùng để gom nhóm rác theo thư mục cha cấp cao.
    """
    for root in get_scan_directories():
        try:
            if root in path.parents:
                return root
        except:
            continue
    return path.parent


def detect_installed_browsers() -> list[str]:
    """
    Xác định các trình duyệt phổ biến đang được cài đặt trên máy người dùng.
    Trả về danh sách như: ['chrome', 'edge', 'firefox', ...]
    """
    home = Path.home()
    browsers = []
    if (home / "AppData/Local/Google/Chrome/User Data").exists():
        browsers.append("chrome")
    if (home / "AppData/Local/Microsoft/Edge/User Data").exists():
        browsers.append("edge")
    if (home / "AppData/Roaming/Mozilla/Firefox/Profiles").exists():
        browsers.append("firefox")
    if (home / "AppData/Local/BraveSoftware/Brave-Browser/User Data").exists():
        browsers.append("brave")
    if (home / "AppData/Roaming/Opera Software").exists():
        browsers.append("opera")
    return browsers


def get_garbage_type(path: Path, installed_browsers: list[str] = None) -> str:
    """
    Phân loại một path thành một trong 12 loại rác hệ thống:
    - Dựa trên tên thư mục, đường dẫn, phần mở rộng
    - Có thể truyền danh sách trình duyệt để phân tích đúng Internet cache, cookies, v.v.

    Returns:
        str: Tên loại rác, hoặc 'Khác' nếu không phân loại được
    """
    p_str = str(path).lower()
    name = path.name.lower()

    if any(b in p_str for b in ["chrome", "edge", "brave", "firefox", "opera"]) and "cache" in p_str:
        return "Internet cache"
    if "cookies" in p_str and any(b in p_str for b in ["chrome", "edge", "firefox", "opera"]):
        return "Cookies"
    if "history" in p_str and any(b in p_str for b in ["chrome", "edge", "firefox", "opera"]):
        return "Internet history"
    if "metrics" in p_str or "telemetry" in p_str:
        return "Metrics temp file"
    if "inetcache" in p_str:
        return "Temporary internet files"
    if "thumbcache" in name:
        return "Thumbnail cache"
    if "$recycle.bin" in p_str:
        return "Empty recycle bin"
    if path.suffix in [".tmp", ".temp", ".~"]:
        return "Temporary files"
    if path.suffix == ".dmp" or name == "memory.dmp":
        return "Memory dumps"
    if path.suffix == ".log" and "windows" in p_str:
        return "Windows log files"
    if "webcache" in p_str or "cache2" in p_str:
        return "Windows web cache"
    if "onedrive" in p_str:
        return "Microsoft OneDrive"
    return "Khác"
