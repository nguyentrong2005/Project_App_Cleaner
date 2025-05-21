from core.system_info import get_system_info as get_real_system_info
from core.scanner import TrashScanner

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