## 虛擬環境
- 虛擬環境 > requirements.txt
```
pip freeze -l > requirements.txt 
```

- 安裝 requirements.txt 內容
```
pip install -r requirements.txt
```

## 一、 自動報價系統(Auto_Quote):

## 日誌
- 2024/10/20 : 客戶管理系統 (完成) 
    - 檔案路徑: ./data/customers.xlsx
- 2024/11/08 : 解決客戶管理系統更新時，無法同步其他頁面選項更新。 (完成)

## 轉檔指令
- pyinstaller --onefile --windowed --icon=./image/icon.ico main.py

## 二、 Youtube 下載器(Youtube_Downloader):

## 日誌

## 轉檔指令
1. 查詢customtkinter路徑: pip show customtkinter
2. pyinstaller --noconfirm --onedir --windowed --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  "<Path to Python Script>"

- pyinstaller --noconfirm --onedir --windowed --icon=icon.ico --add-data "d:\users\egg\desktop\tkinter_project\youtube_downloader\env\lib\site-packages/customtkinter;customtkinter/" "main.py"





    