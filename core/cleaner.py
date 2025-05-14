from pathlib import Path
from typing import List, Tuple
from utils.file_utils import delete_path


def clean_garbage(paths: List[Path]) -> Tuple[int, int]:
    """
    Hàm dọn rác: nhận danh sách các file/thư mục rác và xóa chúng.
    Trả về:
        - Số lượng mục đã xóa thành công
        - Tổng dung lượng đã giải phóng (bytes)
    """
    deleted_count = 0
    freed_space = 0

    for path in paths:
        try:
            size = path.stat().st_size if path.is_file() else 0
            if delete_path(path):
                deleted_count += 1
                freed_space += size
        except Exception:
            continue  # Bỏ qua nếu lỗi khi truy cập

    return deleted_count, freed_space


# ✅ Ví dụ test nhanh
if __name__ == "__main__":
    from core.scanner import TrashScanner

    scanner = TrashScanner()
    rác, tổng_dung_lượng = scanner.scan_garbage()

    print(f"\n🔍 Quét xong: {len(rác)} mục, tổng {tổng_dung_lượng / 1024:.2f} KB")
    đã_xóa, đã_giải_phóng = clean_garbage(rác)
    print(f"\n🧹 Đã xóa: {đã_xóa} mục, giải phóng {đã_giải_phóng / 1024:.2f} KB")
