# core/__init__.py

"""
Core package của CleanerApp
Chứa các thành phần xử lý chính:
- Quét rác (scanner)
- Dọn rác (cleaner)
- Luật xác định file rác (rules)
"""

from .scanner import TrashScanner, scan_and_log
# from .cleaner import clean_garbage
from .rules import is_garbage_file, is_empty_directory, is_writable