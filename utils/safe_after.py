"""
Module `safe_after` - cung cấp các hàm an toàn để sử dụng Tkinter `.after()`

Vấn đề:
- Khi sử dụng `widget.after()` mà widget đã bị `.destroy()`, Tkinter sẽ ném lỗi "invalid command name".
- Điều này thường xảy ra khi lập lịch callback trong giao diện động như loading, animation, ...

Giải pháp:
- `safe_after`: Kiểm tra widget còn tồn tại trước khi lập lịch callback
- `safe_run`: Thực thi callback an toàn, đảm bảo widget vẫn còn hoạt động

Sử dụng:
    from utils.safe_after import safe_after

    safe_after(my_widget, 1000, update_ui)
"""


def safe_after(widget, delay, callback, *args):
    """
    Lập lịch thực thi callback sau một khoảng delay (ms) nếu widget còn tồn tại.

    Args:
        widget (tk.Widget): Widget đang sử dụng .after()
        delay (int): Thời gian delay tính bằng milliseconds
        callback (callable): Hàm callback muốn gọi
        *args: Các đối số truyền vào callback

    Returns:
        int | None: ID của after nếu được gọi thành công, None nếu bị bỏ qua
    """
    if widget.winfo_exists():
        try:
            return widget.after(delay, lambda: safe_run(widget, callback, *args))
        except Exception as e:
            print(f"[SAFE_AFTER ERROR]: {e}")
    else:
        print(f"[AFTER SKIPPED] Widget {widget} no longer exists.")


def safe_run(widget, callback, *args):
    """
    Gọi callback nếu widget vẫn còn tồn tại.

    Args:
        widget (tk.Widget): Widget liên quan đến callback
        callback (callable): Hàm sẽ được gọi
        *args: Đối số cho callback
    """
    try:
        if widget.winfo_exists():
            callback(*args)
    except Exception as e:
        print(f"[SAFE CALLBACK ERROR from {callback.__name__}]: {e}")
