@echo off
echo Building CleanerApp...
pyinstaller ^
--noconfirm ^
--onefile ^
--windowed ^
--icon=assets/images/logo.ico ^
--name CleanerApp ^
main.py
echo Done. File created: dist\CleanerApp.exe
pause
