# utils/__init__.py

"""
Module tiện ích cho CleanerApp.
Tự động import các hàm kiểm tra phổ biến để sử dụng dễ hơn:
- can_delete
- is_file_locked
- check_permissions
"""

from .file_utils import can_delete, is_file_locked, check_permissions