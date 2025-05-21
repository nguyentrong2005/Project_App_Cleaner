import platform
import psutil

def get_system_info() -> str:
    """
    Thu thập thông tin hệ thống thật: OS, CPU, RAM, pin, tất cả ổ đĩa.
    """
    os_name = platform.system() + " " + platform.release()
    cpu = platform.processor() or "Không rõ"
    ram = round(psutil.virtual_memory().total / (1024 ** 3), 1)
    battery = psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A"

    # Lấy danh sách tất cả ổ đĩa
    disk_info_lines = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            total_gb = usage.total / (1024 ** 3)
            disk_info_lines.append(f"📂 Ổ {part.device} — {total_gb:.0f} GB")
        except PermissionError:
            continue  # Một số ổ bảo vệ sẽ không truy cập được

    disk_info = "\n".join(disk_info_lines)

    return (
        f"💻 Hệ điều hành: {os_name}\n"
        f"🧠 CPU: {cpu}\n"
        f"💾 RAM: {ram} GB\n"
        f"{disk_info}\n"
        f"🔋 Pin: {battery}%"
    )
