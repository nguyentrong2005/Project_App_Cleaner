@echo off
echo [*] Building CleanerApp...

REM Build the executable using PyInstaller
pyinstaller ^
--noconfirm ^
--onefile ^
--windowed ^
--name CleanerApp ^
--icon=assets/images/logo.ico ^
--add-data "assets/images;assets/images" ^
main.py

echo [✔] Done. File created at: dist\CleanerApp.exe
pause
