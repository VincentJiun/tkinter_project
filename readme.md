# 一、 自動報價系統(Auto_Quote):

## 日誌
- 2024/10/20 : 客戶管理系統 (完成) 
    - 檔案路徑: ./data/customers.xlsx

## 轉檔指令
- pyinstaller --onefile --windowed --icon=./image/icon.ico main.py

# 二、 Youtube 下載器(Youtube_Downloader):

## 日誌

## 轉檔指令
1. 查詢customtkinter路徑: pip show customtkinter
2. pyinstaller --noconfirm --onedir --windowed --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  "<Path to Python Script>"

- pyinstaller --noconfirm --onedir --windowed --icon=icon.ico --add-data "c:\users\egghead\appdata\local\packages\pythonsoftwarefoundation.python.3.10_qbz5n2kfra8p0\localcache\local-packages\python310\site-packages/customtkinter;customtkinter/" "main.py"





    