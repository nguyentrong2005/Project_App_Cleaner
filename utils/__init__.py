"""
Module `utils` của CleanerApp.

Chứa các hàm tiện ích liên quan đến thao tác hệ thống:
- is_file_locked(path): Kiểm tra xem một file có đang bị chương trình khác sử dụng không
- check_permissions(path): Trả về từ điển mô tả các quyền hệ thống (read, write, execute, delete) trên path

Các hàm này được sử dụng trong quá trình xác định khả năng xóa file/thư mục rác.
"""

from .file_utils import is_file_locked, check_permissions
