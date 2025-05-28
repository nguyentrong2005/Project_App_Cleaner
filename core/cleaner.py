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


def save_clean_history(deleted_paths: list[Path]) -> None:
    """
    Ghi lịch sử xóa rác vào file docs/history_clean.txt
    """
    if not deleted_paths:
        return

    os.makedirs("docs", exist_ok=True)
    with open("docs/history_clean.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(f"\n🧹 Dọn rác lúc {timestamp} ({len(deleted_paths)} mục):\n")
        for p in deleted_paths:
            f.write(f"- {str(p)}\n")


def save_clean_type_history(type_summary: dict[str, list[Path]]) -> None:
    """
    Lưu lịch sử xóa rác theo từng loại vào file docs/history_clean_type.txt.
    """
    if not type_summary:
        return

    os.makedirs("docs", exist_ok=True)
    with open("docs/history_clean_type.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(f"\n🧹 Dọn rác lúc {timestamp}:\n")
        for trash_type, paths in type_summary.items():
            if paths:
                f.write(f"- {trash_type} (xóa {len(paths)} file)\n")


def save_clean_detailed_log(deleted_paths: list[Path]) -> None:
    """
    Ghi danh sách các file đã xóa vào file riêng trong thư mục cleaner/.
    Tên file là thời gian xóa (theo định dạng yyyy-mm-dd_HH-MM-SS.txt).
    """
    if not deleted_paths:
        return

    os.makedirs("docs/cleaner", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = Path(f"docs/cleaner/{timestamp}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"🧹 Dọn rác lúc {timestamp.replace('_', ' ')}:\n")
        for p in deleted_paths:
            f.write(f"- {str(p)}\n")
