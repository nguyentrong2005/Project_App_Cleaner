import os
from pathlib import Path
from typing import List, Tuple
from collections import defaultdict
from time import time
from datetime import datetime

from core.rules import (
    GARBAGE_EXTENSIONS,
    get_scan_directories,
    is_empty_directory,
    can_delete,
    check_permissions,
    get_grouping_root
)
from utils import is_file_locked


class TrashScanner:
    """
    Lớp thực hiện quét file và thư mục rác trong hệ thống.

    Chức năng:
    - Quét đệ quy các thư mục được cấu hình trong rules.py
    - Phân loại file/thư mục nào là rác dựa trên đuôi mở rộng và kích thước
    - Kiểm tra quyền truy cập và trạng thái khóa file
    - Lưu kết quả vào danh sách trash_paths và rejected_paths
    """

    def __init__(self):
        """
        Khởi tạo đối tượng TrashScanner với các thuộc tính lưu kết quả:
        - trash_paths: Danh sách file/thư mục rác có thể xóa
        - total_size: Tổng dung lượng rác đã quét được (đơn vị byte)
        - rejected_paths: Danh sách các path không thể xử lý do thiếu quyền hoặc bị khóa
        """
        self.trash_paths: List[Path] = []
        self.total_size: int = 0
        self.rejected_paths: List[Tuple[Path, dict]] = []

    def scan_garbage(self) -> Tuple[List[Path], int]:
        """
        Thực hiện quét toàn bộ các thư mục được chỉ định trong rules.py
        để tìm file/thư mục rác.

        Returns:
            Tuple[List[Path], int]: Danh sách path rác và tổng dung lượng
        """
        scan_paths = get_scan_directories()

        for path in scan_paths:
            self._scan_directory(path)

        return self.trash_paths, self.total_size

    def _scan_directory(self, folder: Path) -> None:
        """
        Duyệt đệ quy thư mục để kiểm tra file và thư mục rác.
        Lưu kết quả vào trash_paths và rejected_paths.

        Args:
            folder (Path): Thư mục gốc cần quét
        """
        if not folder.exists():
            return

        try:
            for root, dirs, files in os.walk(folder):
                root_path = Path(root)

                # Xử lý file rác
                for file in files:
                    file_path = root_path / file

                    # Bỏ qua nếu không phải file rác
                    if file_path.suffix.lower() not in (ext.lower() for ext in GARBAGE_EXTENSIONS):
                        continue

                    try:
                        stat = file_path.stat()
                        size = stat.st_size
                    except Exception:
                        continue

                    if not can_delete(file_path) or is_file_locked(file_path):
                        self.rejected_paths.append(
                            (file_path, check_permissions(file_path)))
                        continue

                    self.trash_paths.append(file_path)
                    self.total_size += size

                # Xử lý thư mục rỗng
                for dir_name in dirs:
                    dir_path = root_path / dir_name

                    try:
                        if is_empty_directory(dir_path):
                            if can_delete(dir_path):
                                self.trash_paths.append(dir_path)
                            else:
                                self.rejected_paths.append(
                                    (dir_path, check_permissions(dir_path)))
                    except Exception:
                        continue
        except Exception:
            pass


def scan_and_log() -> None:
    """
    Hàm chính để thực hiện toàn bộ quá trình:
    - Quét rác hệ thống bằng TrashScanner
    - Gom nhóm kết quả theo thư mục gốc cấp cao (dựa vào rules.get_grouping_root)
    - Ghi log chi tiết vào file 'docs/scan_log.txt'
    - In tổng kết số lượng, dung lượng rác và thời gian hoàn thành ra console
    """
    os.makedirs("docs", exist_ok=True)
    log_path = Path("docs/scan_log.txt")
    if log_path.exists():
        log_path.unlink()

    start_time = time()
    scanner = TrashScanner()
    paths, total_size = scanner.scan_garbage()
    duration = time() - start_time
    completed_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    grouped: dict[Path, List[Path]] = defaultdict(list)
    for path in paths:
        group_root = get_grouping_root(path)
        grouped[group_root].append(path)

    print(f"🧹 Đã tìm thấy {len(paths)} file/thư mục rác.")
    print(f"📦 Tổng dung lượng: {total_size / 1024:.2f} KB")
    print(f"⏱️ Thời gian quét: {duration:.2f} giây")
    print(f"✅ Hoàn thành lúc: {completed_at}")

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Đã tìm thấy {len(paths)} file/thư mục rác.\n")
        f.write(f"Tổng dung lượng: {total_size / 1024:.2f} KB\n")
        f.write(f"Thời gian quét: {duration:.2f} giây\n")
        f.write(f"Hoàn thành lúc: {completed_at}\n\n")
        f.write("📂 Danh sách rác theo từng thư mục:\n\n")

        for folder, items in sorted(grouped.items()):
            count = len(items)
            size = 0
            for p in items:
                try:
                    size += p.stat().st_size
                except Exception:
                    pass

            f.write(f"📁 {folder}\n")
            f.write(f"  - {count} file/thư mục rác ({size / 1024:.2f} KB)\n")

            for p in items:
                try:
                    sz = p.stat().st_size / 1024 if p.is_file() else 0
                    f.write(f"    • {p.name} ({sz:.2f} KB)\n")
                except Exception:
                    f.write(f"    • {p.name} (Không lấy được dung lượng)\n")
            f.write("\n")

        if scanner.rejected_paths:
            f.write(
                "⚠️ Các file/thư mục KHÔNG được thêm do thiếu quyền hoặc bị khóa:\n")
            for p, perms in scanner.rejected_paths:
                f.write(f"- {p} → Quyền: {perms}\n")

    print("📄 Đã lưu danh sách vào: docs/scan_log.txt")
    return grouped, total_size

