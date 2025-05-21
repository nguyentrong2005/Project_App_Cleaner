# scanner.py
"""
Module quét hệ thống tìm rác cho CleanerApp.

Bao gồm:
- TrashScanner: quét file/thư mục rác
- Phân loại rác theo 12 nhóm
- Ghi kết quả ra file và lịch sử quét
"""

import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from time import time
from typing import List, Tuple
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
    Lớp quét hệ thống và phân loại file/thư mục rác thành 12 nhóm cụ thể.

    Các kết quả được gom vào:
    - self.trash_paths: Danh sách path có thể xóa
    - self.classified_paths: Dict chứa danh sách path theo từng loại rác
    - self.rejected_paths: Danh sách path không thể xóa (bị khóa/thiếu quyền)
    """

    def __init__(self):
        """
        Khởi tạo scanner và khởi tạo danh sách kết quả.
        Tự động phát hiện trình duyệt để phân tích loại rác chính xác hơn.
        """
        self.trash_paths: List[Path] = []
        self.total_size: int = 0
        self.rejected_paths: List[Tuple[Path, dict]] = []
        self.classified_paths: dict[str, List[Path]] = defaultdict(list)
        self.installed_browsers = detect_installed_browsers()
        self.scan_duration = 0

    def scan_garbage(self) -> Tuple[List[Path], int]:
        """
        Thực hiện quét tất cả thư mục đã cấu hình để tìm file/thư mục rác.

        Returns:
            Tuple[List[Path], int]: Danh sách path rác và tổng dung lượng đã quét được.
        """
        start = time()
        scan_dirs = get_scan_directories()
        for folder in scan_dirs:
            self._scan_directory(folder)
        self.scan_duration = time() - start
        return self.trash_paths, self.total_size

    def _scan_directory(self, root: Path) -> None:
        """
        Quét đệ quy một thư mục, kiểm tra và phân loại rác bên trong.

        Args:
            root (Path): Đường dẫn thư mục cần quét
        """
        if not root.exists():
            return

        try:
            for dirpath, dirnames, filenames in os.walk(root):
                current = Path(dirpath)

                # Quét file rác
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

                # Quét thư mục rỗng
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
        Tạo bảng tổng hợp số lượng và dung lượng theo từng loại rác.

        Returns:
            dict: {loại_rác: (số lượng, tổng_dung_lượng_byte)}
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
        Lưu kết quả quét rác vào thư mục docs/scanner.
        - Xóa thư mục cũ nếu có
        - Tạo file `scan_summary.txt` với tổng kết
        - Tạo thư mục `chi_tiet_rac/` chứa file chi tiết từng loại
        - Lưu lịch sử lần quét vào docs/history.txt
        """
        # Xóa dữ liệu cũ
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

<<<<<<< HEAD
    print("📄 Đã lưu danh sách vào: docs/scan_log.txt")
    return grouped, total_size

=======
                filename = rtype.lower().replace(" ", "_") + ".txt"
                detail_path = scanner_dir / "chi_tiet_rac" / filename
                with open(detail_path, "w", encoding="utf-8") as df:
                    for path in self.classified_paths.get(rtype, []):
                        try:
                            size_kb = path.stat().st_size / 1024 if path.is_file() else 0
                            df.write(f"{path} ({size_kb:.2f} KB)\n")
                        except:
                            df.write(f"{path} (Không lấy được dung lượng)\n")

        # Lưu lịch sử
        history_path = Path("docs/history_scan.txt")
        with open(history_path, "a", encoding="utf-8") as hf:
            hf.write(
                f"{time_str} | {len(self.trash_paths)} file | {self.total_size / 1024:.2f} KB\n")


def run_scan():
    """
    Hàm dùng trong main.py để chạy quét rác:
    - Quét hệ thống
    - Lưu kết quả vào thư mục docs/scanner/
    - In thông tin cơ bản ra console
    """
    scanner = TrashScanner()
    scanner.scan_garbage()
    scanner.export_scan_result()

    print(f"🔍 Đã quét {len(scanner.trash_paths)} file/thư mục rác.")
    print(f"📦 Tổng dung lượng: {scanner.total_size / 1024:.2f} KB")
    print(f"🕒 Thời gian quét: {scanner.scan_duration:.2f} giây")
    print("📄 Chi tiết đã lưu trong: docs/scanner/")
>>>>>>> trongdepzai
