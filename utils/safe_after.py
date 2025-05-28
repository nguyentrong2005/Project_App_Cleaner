def safe_after(widget, delay, callback, *args):
    """
    Gọi widget.after(delay, callback) nhưng kiểm tra widget có còn tồn tại không.
    Tránh lỗi 'invalid command name' khi widget đã bị destroy.
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
    Chạy callback nếu widget còn tồn tại.
    """
    try:
        if widget.winfo_exists():
            callback(*args)
    except Exception as e:
        print(f"[SAFE CALLBACK ERROR from {callback.__name__}]: {e}")
