# scanner.py
"""
Module quét hệ thống tìm rác cho CleanerApp.
Tối ưu hóa hiệu suất bằng đa luồng và giới hạn độ sâu quét.
"""

import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from time import time
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor

from core.rules import (
    get_scan_directories,
    is_empty_directory,
    is_garbage_file,
    can_delete,
    check_permissions,
    get_grouping_root,
    get_garbage_type,
    detect_installed_browsers,
    GARBAGE_TYPES
)
from utils import is_file_locked


class TrashScanner:
    """
    Lớp chịu trách nhiệm quét hệ thống để phát hiện file/thư mục rác.

    Tính năng:
    - Duyệt thư mục bằng đa luồng
    - Phân loại thành 12 nhóm rác chuẩn
    - Giới hạn độ sâu để tránh quét sâu gây chậm
    - Ghi log và thống kê chi tiết sau khi quét
    """

    def __init__(self):
        """
        Khởi tạo các biến lưu kết quả:
        - trash_paths: Danh sách path rác đã xác định
        - total_size: Tổng dung lượng rác
        - rejected_paths: Danh sách không thể xóa
        - classified_paths: Gom rác theo loại
        - installed_browsers: Trình duyệt được cài
        - scan_duration: Thời gian quét thực tế
        """
        self.trash_paths: List[Path] = []
        self.total_size: int = 0
        self.rejected_paths: List[Tuple[Path, dict]] = []
        self.classified_paths: dict[str, List[Path]] = defaultdict(list)
        self.installed_browsers = detect_installed_browsers()
        self.scan_duration = 0

    def scan_garbage(self) -> Tuple[List[Path], int]:
        """
        Tiến hành quét hệ thống sử dụng đa luồng để tăng tốc độ.

        Returns:
            Tuple[List[Path], int]: Danh sách file/thư mục rác và tổng dung lượng.
        """
        start = time()
        scan_dirs = get_scan_directories()
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(self._scan_directory, scan_dirs)
        self.scan_duration = time() - start
        return self.trash_paths, self.total_size

    def _scan_directory(self, root: Path, max_depth: int = 6) -> None:
        """
        Đệ quy duyệt thư mục để kiểm tra file/thư mục rác trong thư mục `root`.

        Args:
            root (Path): Thư mục gốc cần quét
            max_depth (int): Giới hạn chiều sâu đệ quy để tránh quá sâu
        """
        if not root.exists() or not root.is_dir():
            return

        try:
            for dirpath, dirnames, filenames in os.walk(root):
                rel = Path(dirpath).relative_to(root)
                if len(rel.parts) > max_depth:
                    dirnames[:] = []  # không đi sâu hơn
                    continue

                # print(f"📁 Đang quét: {dirpath}")
                current = Path(dirpath)

                for fname in filenames:
                    fpath = current / fname
                    if not is_garbage_file(fpath):
                        continue
                    if not can_delete(fpath) or is_file_locked(fpath):
                        self.rejected_paths.append(
                            (fpath, check_permissions(fpath)))
                        continue
                    self.trash_paths.append(fpath)
                    self.total_size += fpath.stat().st_size
                    gtype = get_garbage_type(fpath, self.installed_browsers)
                    self.classified_paths[gtype].append(fpath)

                for dname in dirnames:
                    dpath = current / dname
                    if is_empty_directory(dpath):
                        if can_delete(dpath):
                            self.trash_paths.append(dpath)
                            gtype = get_garbage_type(
                                dpath, self.installed_browsers)
                            self.classified_paths[gtype].append(dpath)
                        else:
                            self.rejected_paths.append(
                                (dpath, check_permissions(dpath)))
        except Exception:
            pass

    def get_classified_summary(self) -> dict:
        """
        Trả về thống kê số lượng và dung lượng của từng loại rác.

        Returns:
            dict: {loại_rác: (số lượng, tổng_dung_lượng)}
        """
        summary = {}
        for rtype, paths in self.classified_paths.items():
            total = 0
            for p in paths:
                try:
                    if p.is_file():
                        total += p.stat().st_size
                except:
                    pass
            summary[rtype] = (len(paths), total)
        return summary

    def export_scan_result(self) -> None:
        """
        Ghi kết quả quét rác ra file:
        - scan_summary.txt: tổng kết
        - chi_tiet_rac/<loai>.txt: chi tiết từng loại
        - history.txt: dòng ghi lịch sử quét
        """
        scanner_dir = Path("docs/scanner")
        if scanner_dir.exists():
            for file in scanner_dir.glob("**/*"):
                try:
                    file.unlink()
                except:
                    pass

        now = datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        summary = self.get_classified_summary()
        os.makedirs("docs/scanner/chi_tiet_rac", exist_ok=True)

        main_log = scanner_dir / "scan_summary.txt"
        with open(main_log, "w", encoding="utf-8") as f:
            f.write(f"Thời gian hoàn tất: {time_str}\n")
            f.write(f"Tổng số file rác: {len(self.trash_paths)}\n")
            f.write(f"Tổng dung lượng: {self.total_size / 1024:.2f} KB\n")
            f.write(f"Thời gian quét: {self.scan_duration:.2f} giây\n\n")

            for rtype in GARBAGE_TYPES:
                count, size = summary.get(rtype, (0, 0))
                f.write(f"- {rtype}: {count} mục, {size / 1024:.2f} KB\n")
                filename = rtype.lower().replace(" ", "_") + ".txt"
                detail_path = scanner_dir / "chi_tiet_rac" / filename
                with open(detail_path, "w", encoding="utf-8") as df:
                    for path in self.classified_paths.get(rtype, []):
                        try:
                            size_kb = path.stat().st_size / 1024 if path.is_file() else 0
                            df.write(f"{path} ({size_kb:.2f} KB)\n")
                        except:
                            df.write(f"{path} (Không lấy được dung lượng)\n")

        history_path = Path("docs/history.txt")
        with open(history_path, "a", encoding="utf-8") as hf:
            hf.write(
                f"{time_str} | {len(self.trash_paths)} file | {self.total_size / 1024:.2f} KB\n")


def run_scan():
    """
    Hàm dùng để chạy thử quá trình quét:
    - Gọi TrashScanner
    - Xuất kết quả
    - In thống kê ra console
    """
    scanner = TrashScanner()
    scanner.scan_garbage()
    scanner.export_scan_result()
    print(f"🔍 Đã quét {len(scanner.trash_paths)} file/thư mục rác.")
    print(f"📦 Tổng dung lượng: {scanner.total_size / 1024:.2f} KB")
    print(f"🕒 Thời gian quét: {scanner.scan_duration:.2f} giây")
    print("📄 Chi tiết đã lưu trong: docs/scanner/")
