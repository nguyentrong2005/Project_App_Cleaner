# localization.py

lang_var = "vi"
callbacks = []

TEXTS = {
    "vi": {
        "home_title": "🧹 Chào mừng đến với App Cleaner",
        "home_desc": "Loại bỏ rác hệ thống để giải phóng dung lượng và tăng hiệu suất máy.",
        "home_tip": "💡 Mẹo: Dọn rác định kỳ giúp máy hoạt động ổn định và nhanh hơn.",
        "home_system": "🖥 Xem thông tin hệ thống",
        "home_os": "💻 Hệ điều hành",
        "home_disk": "📂 Ổ đĩa",
        "home_battery": "🔋 Pin",
        # SCAN
        "scan_label": "Quét",
        "scan_title": "🔍 Quét hệ thống",
        "scan_desc": "Hệ thống sẽ tìm và liệt kê các loại rác cần xóa.",
        "scan_start": "▶ Bắt đầu quét",
        "scan_progress": "Đang quét",
        "scan_done": "✅ Quét hoàn tất",
        "scan_clean": "🧹 Dọn",
        "scan_back": "🔙 Quay lại",
        "scan_select_all": "Chọn tất cả",
        "scan_no_selection": "Vui lòng chọn loại file rác để dọn.",
        "scan_confirm_delete": "Bạn có chắc muốn xoá {n} file đã chọn?",
        "scan_deleted": "✅ Đã xoá {n} file thành công 🎉",
        "scan_col_size": "Dung lượng",
        "scan_col_count": "Số lượng",
        "clean_title": "Dọn rác hệ thống",
        "history_title": "📜 Lịch sử dọn dẹp",
        "history_desc": "Dưới đây là các lần dọn hệ thống gần nhất:",
        "settings_title": "⚙️ Cài đặt ứng dụng",
        "theme": "🎨 Chế độ giao diện:",
        "color": "🌈 Màu chủ đạo:",
        "language": "🌐 Ngôn ngữ:",
        "sound": "🔊 Âm thanh:",
        "section_system": "Hệ thống",
        "home_label": "Trang chủ",
        "settings_label": "Cài đặt",
        "history_label": "Lịch sử",
        "history_col_time": "🕒 Thời gian",
        "history_col_items": "🧹 Số mục",
        "history_col_size": "💾 Dung lượng",
        "detail_col_path": "Đường dẫn",
        "detail_col_size": "Kích thước",
        "dark": "Tối",
        "light": "Sáng",
        "lang_vi": "Tiếng Việt",
        "lang_en": "Tiếng Anh",
        "lang_changed_title": "Ngôn ngữ",
        "lang_changed_msg": "Đã chuyển sang {lang}",
        "exit_label": "Thoát"
    },
    "en": {
        "home_title": "🧹 Welcome to App Cleaner",
        "home_desc": "Remove system junk to free up space and improve performance.",
        "home_tip": "💡 Tip: Regular cleaning keeps your system fast and stable.",
        "home_system": "🖥 View System Info",
        "home_os": "💻 Operating System",
        "home_disk": "📂 Disk",
        "home_battery": "🔋 Battery",
         # SCAN
        "scan_label": "Scan",
        "scan_title": "🔍 System Scan",
        "scan_desc": "The system will scan and list removable junk files.",
        "scan_start": "▶ Start Scan",
        "scan_progress": "Scanning",
        "scan_done": "✅ Scan completed",
        "scan_clean": "🧹 Clean",
        "scan_back": "🔙 Back",
        "scan_select_all": "Select All",
        "scan_no_selection": "Please select at least one file type to clean.",
        "scan_confirm_delete": "Are you sure you want to delete {n} selected files?",
        "scan_deleted": "✅ Successfully deleted {n} files 🎉",
        "scan_col_size": "Size",
        "scan_col_count": "Count",
        "clean_title": "System Cleanup",
        "history_title": "📜 Cleanup History",
        "history_desc": "Recent system cleanup records:",
        "settings_title": "⚙️ App Settings",
        "theme": "🎨 Theme:",
        "color": "🌈 Primary Color:",
        "language": "🌐 Language:",
        "sound": "🔊 Sound:",
        "section_system": "System",
        "home_label": "Home",
        "settings_label": "Settings",
        "history_label": "History",
        "history_col_time": "🕒 Time",
        "history_col_items": "🧹 Items",
        "history_col_size": "💾 Size",
        "detail_col_path": "Path",
        "detail_col_size": "Size",
        "dark": "Dark",
        "light": "Light",
        "lang_vi": "Vietnamese",
        "lang_en": "English",
        "lang_changed_title": "Language",
        "lang_changed_msg": "Switched to {lang}",
        "exit_label": "Exit"
    }
}


def tr(key):
    """
    Lấy chuỗi đã dịch theo khóa `key`, tương ứng với ngôn ngữ hiện tại.

    Args:
        key (str): Tên khóa ngôn ngữ (vd: "home_title")

    Returns:
        str: Chuỗi đã dịch nếu có, hoặc chính key nếu không tìm thấy
    """
    return TEXTS.get(lang_var, TEXTS["vi"]).get(key, key)


def set_language(lang_code):
    """
    Đặt lại ngôn ngữ hiển thị cho toàn bộ ứng dụng.

    Khi thay đổi ngôn ngữ:
    - Biến `lang_var` sẽ được cập nhật
    - Tất cả các callback đã đăng ký qua `on_language_change()` sẽ được gọi

    Args:
        lang_code (str): Mã ngôn ngữ ("vi" hoặc "en")
    """
    global lang_var
    lang_var = lang_code
    for cb in callbacks:
        cb()


def on_language_change(callback):
    """
    Đăng ký hàm callback để được gọi mỗi khi ngôn ngữ thay đổi.

    Dùng trong UI để tự động cập nhật lại nội dung khi đổi ngôn ngữ.

    Args:
        callback (function): Hàm cần gọi lại khi ngôn ngữ thay đổi
    """
    callbacks.append(callback)
