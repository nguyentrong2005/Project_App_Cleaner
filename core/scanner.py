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
    Lớp chịu trách nhiệm quét hệ thống để phát hiện và phân loại file/thư mục rác.

    Tính năng:
    - Duyệt thư mục bằng đa luồng
    - Phân loại thành 12 nhóm rác chuẩn
    - Giới hạn độ sâu đệ quy để tăng hiệu năng
    - Ghi log và thống kê chi tiết sau khi quét
    """

    def __init__(self):
        """
        Khởi tạo các thuộc tính để lưu kết quả quét.
        """
        self.trash_paths: List[Path] = []
        self.total_size: int = 0
        self.rejected_paths: List[Tuple[Path, dict]] = []
        self.classified_paths: dict[str, List[Path]] = defaultdict(list)
        self.installed_browsers = detect_installed_browsers()
        self.scan_duration = 0

    def scan_garbage(self) -> Tuple[List[Path], int]:
        """
        Quét hệ thống tìm các file/thư mục rác bằng đa luồng.

        Returns:
            Tuple[List[Path], int]: Danh sách file/thư mục rác và tổng dung lượng rác.
        """
        start = time()
        scan_dirs = get_scan_directories()
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(self._scan_directory, scan_dirs)
        self.scan_duration = time() - start
        return self.trash_paths, self.total_size

    def _scan_directory(self, root: Path, max_depth: int = 6) -> None:
        """
        Đệ quy duyệt và xử lý file/thư mục rác trong thư mục `root`.

        Args:
            root (Path): Thư mục gốc cần quét.
            max_depth (int): Chiều sâu tối đa khi đệ quy.
        """
        if not root.exists() or not root.is_dir():
            return

        try:
            for dirpath, dirnames, filenames in os.walk(root):
                rel = Path(dirpath).relative_to(root)
                if len(rel.parts) > max_depth:
                    dirnames[:] = []  # Ngăn không đệ quy sâu hơn
                    continue

                current = Path(dirpath)

                # Xử lý file
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

                # Xử lý thư mục rỗng
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
            pass  # Giữ chương trình chạy nếu có lỗi đọc thư mục

    def get_classified_summary(self) -> dict[str, Tuple[int, int]]:
        """
        Tạo thống kê số lượng và dung lượng cho từng loại rác.

        Returns:
            dict[str, Tuple[int, int]]: {loại_rác: (số lượng, tổng_dung_lượng_bytes)}
        """
        summary = {}
        for rtype, paths in self.classified_paths.items():
            total_size = 0
            for p in paths:
                try:
                    if p.is_file():
                        total_size += p.stat().st_size
                except:
                    pass
            summary[rtype] = (len(paths), total_size)
        return summary

    def export_scan_result(self) -> None:
        """
        Xuất kết quả quét ra file:
        - `scan_summary.txt`: thống kê chung
        - `chi_tiet_rac/<loai>.txt`: danh sách file theo từng loại
        - `history.txt`: ghi lại lịch sử quét (nếu cần)
        """
        scanner_dir = Path("docs/scanner")
        if scanner_dir.exists():
            for file in scanner_dir.glob("**/*"):
                try:
                    file.unlink()
                except:
                    pass

        os.makedirs("docs/scanner/chi_tiet_rac", exist_ok=True)
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary = self.get_classified_summary()

        with open(scanner_dir / "scan_summary.txt", "w", encoding="utf-8") as f:
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


def run_scan():
    """
    Hàm chạy thử (debug) cho quá trình quét:
    - Gọi TrashScanner
    - Xuất kết quả ra file
    - In thống kê ra console
    """
    scanner = TrashScanner()
    scanner.scan_garbage()
    scanner.export_scan_result()

    print(f"🔍 Đã quét {len(scanner.trash_paths)} file/thư mục rác.")
    print(f"📦 Tổng dung lượng: {scanner.total_size / 1024:.2f} KB")
    print(f"🕒 Thời gian quét: {scanner.scan_duration:.2f} giây")
    print("📄 Chi tiết đã lưu trong: docs/scanner/")
