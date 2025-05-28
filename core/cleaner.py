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
from core.rules import can_delete
from utils import is_file_locked
from datetime import datetime


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

def save_clean_summary_log(type_summary):
    """
    Ghi vào history_cleaner.txt với số lượng, dung lượng, loại rác đã xóa.
    type_summary: dict[str, list[Tuple[Path, int]]] – mỗi phần tử là (đường dẫn, size)
    """
    from datetime import datetime

    os.makedirs("docs/cleaner", exist_ok=True)
    with open("docs/cleaner/history_cleaner.txt", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        total_count = sum(len(l) for l in type_summary.values())
        total_size = sum(sz for l in type_summary.values() for _, sz in l)
        total_size_mb = round(total_size / (1024 * 1024), 1)

        f.write(f"🧹 Dọn rác lúc {now} — Tổng: {total_count} mục, {total_size_mb} MB\n")
        for trash_type, path_tuples in type_summary.items():
            count = len(path_tuples)
            size = sum(sz for _, sz in path_tuples)
            size_mb = round(size / (1024 * 1024), 1)
            f.write(f"- {trash_type}: {count} mục, {size_mb} MB\n")


def save_clean_per_type_detail(type_summary: dict[str, list[Path]]):
    """
    Ghi chi tiết các file đã xóa vào file duy nhất:
    docs/cleaner/chi_tiet_xoa/{timestamp}.txt
    """
    if not type_summary:
        return

    folder = Path("docs/cleaner/chi_tiet_xoa")
    folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = folder / f"{timestamp}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"🧹 Dọn rác lúc {timestamp.replace('_', ' ')}\n\n")
        for trash_type, paths in type_summary.items():
            if not paths:
                continue
            f.write(f"📂 {trash_type} ({len(paths)} mục):\n")
            for p in paths:
                f.write(f"- {str(p)}\n")
            f.write("\n")
