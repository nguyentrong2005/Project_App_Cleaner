import platform
import psutil

def get_system_info() -> str:
    """
    Thu thập thông tin hệ thống thật: OS, CPU, RAM, pin, tất cả ổ đĩa.
    """
    # ⬇️ Import trễ để tránh vòng lặp
    from gui.localization import tr

    os_name = platform.system() + " " + platform.release()
    cpu = platform.processor() or "Không rõ"
    ram = round(psutil.virtual_memory().total / (1024 ** 3), 1)
    battery = psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A"

    disk_info_lines = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            total_gb = usage.total / (1024 ** 3)
            disk_info_lines.append(f"{tr('home_disk')} {part.device} — {total_gb:.0f} GB")
        except PermissionError:
            continue

    disk_info = "\n".join(disk_info_lines)

    return (
        f"{tr('home_os')}: {os_name}\n"
        f"{tr('home_cpu')}: {cpu}\n"
        f"{tr('home_ram')}: {ram} GB\n"
        f"{disk_info}\n"
        f"{tr('home_battery')}: {battery}%"
    )
