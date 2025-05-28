@echo off
echo 🔧 Đang đóng gói CleanerApp thành .exe...

pyinstaller ^
  --noconfirm ^
  --onefile ^
  --windowed ^
  --name CleanerApp ^
  --add-data "docs;docs" ^
  --add-data "assets;assets" ^
  main.py

echo ✅ Đã hoàn tất! File .exe nằm trong thư mục dist\
pause
