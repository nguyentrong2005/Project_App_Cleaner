# localization.py
lang_var = "vi"
callbacks = []

TEXTS = {
    "vi": {
        "home_title": "🧹 Chào mừng đến với App Cleaner",
        "home_desc": "Loại bỏ rác hệ thống để giải phóng dung lượng và tăng hiệu suất máy.",
        "home_tip": "💡 Mẹo: Dọn rác định kỳ giúp máy hoạt động ổn định và nhanh hơn.",
        "scan_title": "Quét hệ thống",
        "scan_desc": "Hệ thống sẽ tìm và liệt kê các tệp rác, shortcut hỏng và registry lỗi.",
        "scan_start": "▶ Bắt đầu quét",
        "clean_title": "Dọn hệ thống",
        "clean_list_title": "Danh sách các mục rác được phát hiện:",
        "clean_button": "⚡ Bắt đầu dọn",
        "history_title": "📜 Lịch sử dọn dẹp",
        "history_desc": "Dưới đây là các lần dọn hệ thống gần nhất:",
        "settings_title": "Cài đặt ứng dụng",
        "theme": "🎨 Chế độ giao diện:",
        "color": "🌈 Màu chủ đạo:",
        "language": "🌐 Ngôn ngữ:",
        "sound": "🔊 Âm thanh:",
        "section_system": "Hệ thống",
       
        "home_label": "Trang chủ",
        "scan_label": "Quét",
        "clean_label": "Dọn",
        "settings_label": "Cài đặt",
        "history_label": "Lịch sử",
        "confirm_clean": "Bạn có chắc chắn muốn dọn dẹp không?",
        "yes": "Có",
        "no": "Không",
        "exit_label": "Thoát"
        

    },
    "en": {
        "home_title": "🧹 Welcome to App Cleaner",
        "home_desc": "Remove system junk to free up space and improve performance.",
        "home_tip": "💡 Tip: Regular cleaning keeps your system fast and stable.",
        "scan_title": "System Scan",
        "scan_desc": "The system will scan for junk files, broken shortcuts, and bad registries.",
        "scan_start": "▶ Start Scan",
        "clean_title": "System Cleaning",
        "clean_list_title": "Detected junk items:",
        "clean_button": "⚡ Start Cleaning",
        "history_title": "📜 Cleanup History",
        "history_desc": "Recent system cleanup records:",
        "settings_title": "App Settings",
        "theme": "🎨 Theme:",
        "color": "🌈 Primary Color:",
        "language": "🌐 Language:",
        "sound": "🔊 Sound:",
        "section_system": "System",
        "home_label": "Home",
        "scan_label": "Scan",
        "clean_label": "Clean",
        "settings_label": "Settings",
        "history_label": "History",
        "confirm_clean": "Are you sure you want to clean?",
        "yes": "Yes",
        "no": "No",
        "exit_label": "Exit"
    }
}

def tr(key):
    return TEXTS.get(lang_var, TEXTS["vi"]).get(key, key)

def set_language(lang_code):
    global lang_var
    lang_var = lang_code
    for cb in callbacks:
        cb()

def on_language_change(callback):
    callbacks.append(callback)
