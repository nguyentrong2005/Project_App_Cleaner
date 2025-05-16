import os
import tempfile
from pathlib import Path
from typing import List, Tuple

from core.rules import is_garbage_file, is_empty_directory, is_writable
from utils import is_file_locked, check_permissions


class TrashScanner:
    """
    Lớp TrashScanner dùng để quét file/thư mục rác an toàn trong hệ thống.
    Chỉ kiểm tra trong các thư mục TEMP của người dùng và Windows.
    """

    def __init__(self):
        self.trash_paths: List[Path] = []
        self.total_size: int = 0
        # Lưu các file không đủ quyền
        self.rejected_paths: List[Tuple[Path, dict]] = []

    def scan_garbage(self) -> Tuple[List[Path], int]:
        """
        Quét các thư mục an toàn để tìm rác.
        Trả về: (danh sách path rác, tổng dung lượng rác)
        """
        safe_paths = [
            Path(tempfile.gettempdir()),       # %TEMP% của user
            Path('C:/Windows/Temp')            # TEMP hệ thống
        ]

        for path in safe_paths:
            self._scan_directory(path)

        return self.trash_paths, self.total_size

    def _scan_directory(self, folder: Path) -> None:
        """Duyệt đệ quy thư mục để kiểm tra file/thư mục rác"""
        if not folder.exists():
            return

        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = Path(root) / file
                if is_garbage_file(file_path):
                    perms = check_permissions(file_path)
                    if perms["delete"] and not is_file_locked(file_path):
                        self.trash_paths.append(file_path)
                        self.total_size += file_path.stat().st_size
                    else:
                        self.rejected_paths.append((file_path, perms))

            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                if is_empty_directory(dir_path):
                    perms = check_permissions(dir_path)
                    if perms["delete"]:
                        self.trash_paths.append(dir_path)
                    else:
                        self.rejected_paths.append((dir_path, perms))


def scan_and_log() -> None:
    os.makedirs("docs", exist_ok=True)
    log_path = Path("docs/scan_log.txt")
    if log_path.exists():
        log_path.unlink()

    scanner = TrashScanner()
    paths, size = scanner.scan_garbage()

    print(f"Đã tìm thấy {len(paths)} file/thư mục rác.")
    print(f"Tổng dung lượng: {size / 1024:.2f} KB")

    os.makedirs("docs", exist_ok=True)
    with open("docs/scan_log.txt", "w", encoding="utf-8") as f:
        f.write(f"Đã tìm thấy {len(paths)} file/thư mục rác.\n")
        f.write(f"Tổng dung lượng: {size / 1024:.2f} KB\n\n")
        f.write("Danh sách file/thư mục có thể xóa:\n")
        for p in paths:
            size_kb = p.stat().st_size / 1024 if p.is_file() else 0
            f.write(f"- {p} ({size_kb:.2f} KB)\n")

        if scanner.rejected_paths:
            f.write("\n⚠️ Các file/thư mục KHÔNG được thêm do thiếu quyền:\n")
            for p, perms in scanner.rejected_paths:
                f.write(f"- {p} → Quyền: {perms}\n")

    print("📄 Đã lưu danh sách vào: docs/scan_log.txt")
