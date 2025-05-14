import os
import tempfile
from pathlib import Path
from typing import List, Tuple


class TrashScanner:
    """
    Quét các file/thư mục rác trong TEMP an toàn:
    - File .tmp, .log, .bak
    - File rỗng
    - Thư mục rỗng
    """

    EXTENSIONS = ['.tmp', '.log', '.bak']

    def __init__(self):
        self.trash_paths: List[Path] = []
        self.total_size: int = 0

        # Dùng để phân loại file rác
        self.tmp_files: List[Path] = []
        self.log_files: List[Path] = []
        self.bak_files: List[Path] = []
        self.empty_files: List[Path] = []
        self.empty_dirs: List[Path] = []

    def scan_garbage(self) -> Tuple[List[Path], int]:
        safe_paths = [
            Path(tempfile.gettempdir()),
            Path("C:/Windows/Temp")
        ]

        for path in safe_paths:
            self._scan_directory(path)

        self.trash_paths = (
            self.tmp_files +
            self.log_files +
            self.bak_files +
            self.empty_files +
            self.empty_dirs
        )
        return self.trash_paths, self.total_size

    def _scan_directory(self, folder: Path) -> None:
        if not folder.exists():
            return

        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = Path(root) / file
                if not os.access(file_path, os.W_OK):
                    continue

                if file_path.suffix.lower() == '.tmp':
                    self.tmp_files.append(file_path)
                    self.total_size += file_path.stat().st_size
                elif file_path.suffix.lower() == '.log':
                    self.log_files.append(file_path)
                    self.total_size += file_path.stat().st_size
                elif file_path.suffix.lower() == '.bak':
                    self.bak_files.append(file_path)
                    self.total_size += file_path.stat().st_size
                elif file_path.stat().st_size == 0:
                    self.empty_files.append(file_path)

            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                if dir_path.exists() and dir_path.is_dir() and not any(dir_path.iterdir()):
                    if os.access(dir_path, os.W_OK):
                        self.empty_dirs.append(dir_path)

    def get_summary_text(self) -> str:
        lines = ["\n🔍 KẾT QUẢ PHÂN LOẠI RÁC:"]

        def _group(label: str, paths: List[Path]):
            lines.append(f"\n{label} ({len(paths)} mục):")
            for p in paths:
                size = p.stat().st_size if p.is_file() else 0
                size_kb = size / 1024
                lines.append(f" - {p} ({size_kb:.2f} KB)")

        _group("📄 File .tmp", self.tmp_files)
        _group("📄 File .log", self.log_files)
        _group("📄 File .bak", self.bak_files)
        _group("⚪ File rỗng", self.empty_files)
        _group("📂 Thư mục rỗng", self.empty_dirs)

        return "\n".join(lines)


if __name__ == "__main__":
    scanner = TrashScanner()
    paths, size = scanner.scan_garbage()

    print(f"\n🔍 Đã tìm thấy {len(paths)} file/thư mục rác.")
    print(f"📦 Tổng dung lượng: {size / 1024:.2f} KB")

    # Ghi kết quả ra file text
    with open("scan_result.txt", "w", encoding="utf-8") as f:
        f.write(f"Đã tìm thấy {len(paths)} file/thư mục rác.\n")
        f.write(f"Tổng dung lượng: {size / 1024:.2f} KB\n")
        f.write(scanner.get_summary_text())

    print("\n📄 Kết quả đã được lưu vào: scan_result.txt")
