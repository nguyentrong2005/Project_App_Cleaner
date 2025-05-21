from core.system_info import get_system_info as get_real_system_info
from core.scanner import TrashScanner
from core.scanner import scan_and_log


def get_system_info() -> str:
    return get_real_system_info()


def scan_garbage_real():
    """
    Gọi lớp TrashScanner để quét file/thư mục rác thực sự.
    Trả về danh sách path và tổng dung lượng (byte)
    """
    scanner = TrashScanner()
    paths, total_size = scanner.scan_garbage()
    return paths, total_size


def scan_and_save_log():
    scan_and_log()

def scan_and_log_and_return():
    return scan_and_log()
