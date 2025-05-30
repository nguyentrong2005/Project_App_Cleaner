# main.py
from gui import run_main_window
from LicenseScreen.license_agreement import show_license_screen

def start_main_app():
    window.mainloop()
    
if __name__ == "__main__":
    show_license_screen(on_accept=start_main_app)
    # run_scan()
