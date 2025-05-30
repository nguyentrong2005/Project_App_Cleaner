from core.system_info import get_system_info as get_real_system_info
from core.scanner import TrashScanner
from core.cleaner import TrashCleaner
from pathlib import Path
from core.cleaner import TrashCleaner


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


def delete_selected_files(file_paths):
    """
    Gọi TrashCleaner để xóa các file đã chọn.

    Args:
        file_paths (List[str]): Danh sách đường dẫn file (dưới dạng chuỗi)

    Returns:
        Tuple[List[str], List[Tuple[str, str]]]: (file xóa thành công, file lỗi + lý do)
    """
    paths = [Path(p) for p in file_paths]
    cleaner = TrashCleaner(paths)
    cleaner.clean()
    deleted, failed = cleaner.get_result()

    # Trả lại ở dạng str cho dễ xử lý trên giao diện
    return [str(p) for p in deleted], [(str(p), reason) for p, reason in failed]

def get_clean_history():
    """
    Đọc lịch sử dọn rác từ file docs/cleaner/history_cleaner.txt.
    Trả về danh sách dòng thời gian xóa: thời gian, tổng số file, tổng dung lượng, các loại rác.
    """
    history_path = Path("docs/cleaner/history_cleaner.txt")
    if not history_path.exists():
        return []

    history = []
    current_time = ""
    summary = []

    with open(history_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("🧹 Dọn rác lúc"):
                # Nếu có dòng trước đó, lưu lại trước
                if current_time:
                    history.append((current_time, summary))
                    summary = []

                parts = line.split("— Tổng:")
                current_time = parts[0].replace("🧹 Dọn rác lúc", "").strip()
                summary.append(parts[1].strip() if len(parts) > 1 else "")
            elif line.startswith("-") or line.startswith("  -"):
                summary.append(line.strip())

        # Lưu dòng cuối
        if current_time:
            history.append((current_time, summary))

    return history

