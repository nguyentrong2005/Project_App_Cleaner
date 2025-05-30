# cleaner.py
"""
Module xóa rác hệ thống cho CleanerApp.

Chức năng chính:
- Nhận danh sách file/thư mục cần xóa
- Kiểm tra quyền truy cập và trạng thái khóa
- Thực hiện xóa và ghi lại kết quả
- Ghi lịch sử dọn dẹp và chi tiết vào file log
"""

import os
from pathlib import Path
from typing import List, Tuple
from datetime import datetime

from core.rules import can_delete
from utils import is_file_locked


class TrashCleaner:
    """
    Lớp thực hiện việc xóa các file/thư mục rác.

    Attributes:
        paths (List[Path]): Danh sách các path cần xóa
        deleted (List[Path]): Danh sách đã xóa thành công
        failed (List[Tuple[Path, str]]): Danh sách lỗi và lý do thất bại
    """

    def __init__(self, paths: List[Path]):
        """
        Khởi tạo TrashCleaner với danh sách cần xóa.

        Args:
            paths (List[Path]): Danh sách file/thư mục rác
        """
        self.paths = paths
        self.deleted: List[Path] = []
        self.failed: List[Tuple[Path, str]] = []

    def clean(self) -> None:
        """
        Xóa từng path trong danh sách:
        - Kiểm tra quyền xóa và trạng thái khóa
        - Ghi lại kết quả vào `deleted` hoặc `failed`
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
        Trả về kết quả sau khi thực hiện dọn dẹp.

        Returns:
            Tuple:
                - Danh sách đã xóa thành công
                - Danh sách lỗi (kèm lý do)
        """
        return self.deleted, self.failed


def save_clean_summary_log(type_summary: dict[str, List[Tuple[Path, int]]]) -> None:
    """
    Ghi log tổng hợp kết quả dọn dẹp vào history_cleaner.txt

    Args:
        type_summary (dict): Dữ liệu dạng {loại_rác: [(path, size_bytes)]}
    """
    os.makedirs("docs/cleaner", exist_ok=True)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    total_count = sum(len(paths) for paths in type_summary.values())
    total_size = sum(size for paths in type_summary.values()
                     for _, size in paths)
    total_size_mb = round(total_size / (1024 * 1024), 1)

    with open("docs/cleaner/history_cleaner.txt", "a", encoding="utf-8") as f:
        f.write(
            f"🧹 Dọn rác lúc {now} — Tổng: {total_count} mục, {total_size_mb} MB\n")
        for trash_type, path_tuples in type_summary.items():
            count = len(path_tuples)
            size = sum(sz for _, sz in path_tuples)
            size_mb = round(size / (1024 * 1024), 1)
            f.write(f"- {trash_type}: {count} mục, {size_mb} MB\n")


def save_clean_per_type_detail(type_summary: dict[str, List[Path]]) -> None:
    """
    Ghi chi tiết các path đã xóa ra 1 file log duy nhất trong docs/cleaner/chi_tiet_xoa/

    Args:
        type_summary (dict): Dữ liệu dạng {loại_rác: [path1, path2, ...]}
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
