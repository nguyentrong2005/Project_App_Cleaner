import tkinter as tk
from gui.main_window import CleanerAppGUI


def main() -> None:
    root = tk.Tk()
    app = CleanerAppGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
