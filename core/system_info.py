import platform
import psutil


def get_system_info() -> str:
    """
    Thu thập và trả về thông tin hệ thống dưới dạng chuỗi.

    Bao gồm:
    - Hệ điều hành (OS)
    - Bộ xử lý (CPU)
    - Dung lượng RAM
    - Mức pin (nếu có)
    - Dung lượng các ổ đĩa

    Trả về:
        str: Chuỗi chứa thông tin hệ thống được dịch theo ngôn ngữ hiện tại.
    """
    # Import tại đây để tránh vòng lặp import với GUI
    from gui.localization import tr

    # Lấy thông tin hệ điều hành và CPU
    os_name = platform.system() + " " + platform.release()
    cpu = platform.processor() or "Không rõ"

    # Lấy dung lượng RAM (đơn vị: GB)
    ram = round(psutil.virtual_memory().total / (1024 ** 3), 1)

    # Lấy mức pin nếu có
    battery_info = psutil.sensors_battery()
    battery = battery_info.percent if battery_info else "N/A"

    # Lấy thông tin ổ đĩa
    disk_info_lines = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            total_gb = usage.total / (1024 ** 3)
            disk_info_lines.append(
                f"{tr('home_disk')} {part.device} — {total_gb:.0f} GB")
        except PermissionError:
            continue  # Bỏ qua phân vùng không có quyền truy cập

    # Gộp thông tin các ổ đĩa lại
    disk_info = "\n".join(disk_info_lines)

    # Trả về thông tin hệ thống dưới dạng chuỗi
    return (
        f"{tr('home_os')}: {os_name}\n"
        f"{tr('home_cpu')}: {cpu}\n"
        f"{tr('home_ram')}: {ram} GB\n"
        f"{disk_info}\n"
        f"{tr('home_battery')}: {battery}%"
    )
