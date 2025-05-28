from core.system_info import get_system_info as get_real_system_info
from core.scanner import TrashScanner
from pathlib import Path


def get_system_info():
    """
    Hàm trung gian gọi thông tin hệ thống từ core.
    Trả về chuỗi mô tả hệ thống thật.
    """
    return get_real_system_info()


def scan_and_return_summary():
    """
    Thực hiện quét rác thật và trả về:
    - summary: dict loại_rác → (số lượng, dung lượng)
    - chi_tiet: dict loại_rác → danh sách file path
    - tổng dung lượng
    - thời gian quét
    """
    scanner = TrashScanner()
    scanner.scan_garbage()
    summary = scanner.get_classified_summary()
    scanner.export_scan_result()

    return summary, scanner.classified_paths, scanner.total_size, scanner.scan_duration


def get_scan_history():
    history_path = Path("docs/history.txt")
    history = []
    if history_path.exists():
        with open(history_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split("|")
                    if len(parts) == 3:
                        time_str = parts[0].strip()
                        items = parts[1].strip()
                        size = parts[2].strip()
                        history.append((time_str, items, size))
    return history
