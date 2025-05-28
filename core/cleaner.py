# cleaner.py
"""
Module xóa rác hệ thống cho CleanerApp.

- Nhận danh sách file/thư mục cần xóa từ quá trình quét
- Kiểm tra quyền truy cập và trạng thái khóa
- Tiến hành xóa và ghi lại kết quả
- Ghi lịch sử dọn dẹp vào file
"""

from pathlib import Path
from typing import List, Tuple
import os
from core.rules import can_delete, check_permissions
from utils import is_file_locked


class TrashCleaner:
    """
    Lớp thực hiện xóa các file/thư mục rác đã được quét.

    Attributes:
        paths (List[Path]): Danh sách path cần xóa
        deleted (List[Path]): Danh sách path đã xóa thành công
        failed (List[Tuple[Path, str]]): Danh sách path bị lỗi kèm lý do
    """

    def __init__(self, paths: List[Path]):
        """
        Khởi tạo TrashCleaner với danh sách path cần xóa.

        Args:
            paths (List[Path]): Danh sách file/thư mục cần xóa
        """
        self.paths = paths
        self.deleted: List[Path] = []
        self.failed: List[Tuple[Path, str]] = []

    def clean(self) -> None:
        """
        Thực hiện xóa tất cả path trong danh sách:

        - Kiểm tra quyền và trạng thái khóa
        - Ghi lại kết quả vào danh sách `deleted` và `failed`
        """
        for path in self.paths:
            try:
                if not path.exists():
                    continue
                if not can_delete(path):
                    self.failed.append((path, "Không đủ quyền"))
                    continue
                if is_file_locked(path):
                    self.failed.append((path, "Tập tin đang bị khóa"))
                    continue

                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    os.rmdir(path)
                self.deleted.append(path)

            except Exception as e:
                self.failed.append((path, str(e)))

    def get_result(self) -> Tuple[List[Path], List[Tuple[Path, str]]]:
        """
        Trả về kết quả sau khi xóa.

        Returns:
            Tuple[List[Path], List[Tuple[Path, str]]]:
                - Danh sách đã xóa
                - Danh sách thất bại (kèm lý do)
        """
        return self.deleted, self.failed


def run_clean():
    """
    Hàm dùng trong main.py để thực hiện toàn bộ quy trình dọn rác:
    - Gọi TrashScanner để quét rác
    - Dọn bằng TrashCleaner
    - Ghi kết quả và lịch sử dọn vào file
    - In kết quả ra console
    """
    from core.scanner import TrashScanner
    from time import time
    from datetime import datetime

    # Quét rác
    scanner = TrashScanner()
    scanner.scan_garbage()

    # Dọn rác
    cleaner = TrashCleaner(scanner.trash_paths)
    print(f"🗑 Đang tiến hành dọn {len(scanner.trash_paths)} mục...")

    start = time()
    cleaner.clean()
    duration = time() - start

    deleted, failed = cleaner.get_result()
    print(f"✅ Đã xóa {len(deleted)} mục trong {duration:.2f} giây.")
    if failed:
        print(f"⚠️ Có {len(failed)} mục không xóa được:")
        for p, reason in failed:
            print(f" - {p} → {reason}")

    # Ghi lịch sử
    history_path = Path("docs/history_clean.txt")
    history_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(history_path, "a", encoding="utf-8") as f:
        f.write(
            f"{now} | ĐÃ DỌN: {len(deleted)} mục | THẤT BẠI: {len(failed)} mục\n")
