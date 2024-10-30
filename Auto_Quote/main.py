import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
from tkcalendar import Calendar
from datetime import datetime
import os
import subprocess

from excel import ExcelCMS, ExcelQuote

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Title, Icon, size
        self.title('德龍企業社')
        self.iconbitmap('./image/icon.ico')
        self.geometry('1280x780')

        # 創建 IndexPage 和 CMSPage 兩個頁面
        self.index_page = IndexPage(self)
        self.cms_page = CMSPage(self)
        self.quote_page = QuotePage(self)
        self.report_page = ReportPage(self)

        # 預設顯示 IndexPage
        self.index_page.pack(fill='both', expand=True)

    def change_page(self, page):
        # 隱藏當前顯示的頁面
        for widget in self.winfo_children():
            widget.pack_forget()

        # 顯示傳入的目標頁面
        page.pack(fill='both', expand=True)

class IndexPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize_ids = {}  # 用於跟踪各個Label的after()事件ID

        self.create_page()  # 在初始化時創建頁面佈局

    def create_page(self):
        # index Frame
        self.frame_container = ttk.Frame(self)
        self.frame_container.pack(fill='both', expand=True)
        
        # index image
        img = Image.open('./image/logo.png')
        self.label_img = tk.Label(self.frame_container)
        self.label_img.place(relx=0.5, rely=0.45, relwidth=0.55, relheight=0.5, anchor='center')
        
        # title
        self.title = tk.Label(self.frame_container, text='德龍企業社', font=('標楷體', 30, 'bold'), fg='#000000')
        self.title.place(relx=0.5, rely=0.1, relheight=0.1, relwidth=0.5, anchor='center')
        
        # buttons
        self.btn_quote = tk.Button(self.frame_container, text='報價單', font=('標楷體', 20, 'bold'), fg='#000000', command=lambda: self.master.change_page(self.master.quote_page))
        self.btn_quote.place(relx=0.25, rely=0.85, relwidth=0.2, relheight=0.1, anchor='center')
        
        self.btn_cms = tk.Button(self.frame_container, text='客戶管理', font=('標楷體', 20, 'bold'), fg='#000000', command=lambda: self.master.change_page(self.master.cms_page))
        self.btn_cms.place(relx=0.5, rely=0.85, relwidth=0.2, relheight=0.1, anchor='center')
        
        self.btn_report = tk.Button(self.frame_container, text='營收報表', font=('標楷體', 20, 'bold'), fg='#000000', command=lambda: self.master.change_page(self.master.report_page))
        self.btn_report.place(relx=0.75, rely=0.85, relwidth=0.2, relheight=0.1, anchor='center')

        self.bind_resize_event(self.label_img, img)

    def bind_resize_event(self, label, image):
        label.bind("<Configure>", lambda event: self.delayed_resize_image(event, label, image))

    def delayed_resize_image(self, event, label, image):
        # 如果該Label已有延迟更新的計劃，取消它
        if label in self.resize_ids:
            self.after_cancel(self.resize_ids[label])

        # 延迟 100 毫秒后调用真正的图片更新函数
        self.resize_ids[label] = self.after(100, lambda: self.resize_image(label, image))

    def resize_image(self, label, img):
        # 获取 Label 的宽度和高度
        width, height = label.winfo_width(), label.winfo_height()

        if width > 0 and height > 0:  # 确保宽高有效
            # 按照 Label 尺寸调整图片大小
            resized_image = img.resize((width, height))
            tk_image = ImageTk.PhotoImage(resized_image)

            # 更新 Label 中的图片
            label.config(image=tk_image)
            label.image = tk_image  # 保留引用，防止图片被垃圾回收

class CMSPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.cms_datas = []
        self.selected_item_index = None  # 用於記錄選中的客戶索引

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('標楷體', 14, 'bold'), foreground='black')
        style.map("Treeview.Heading", background=[('active', '#FFD700')])
        style.configure("Treeview.Heading", background='#FFD700')

        self.create_page()  # 初始化時創建佈局

        try:
            self.excel_cms = ExcelCMS('customers.xlsx')
            self.cms_datas = self.excel_cms.read_all_datas()
            if not self.cms_datas:
                print("Warning: No data found in Excel file.")
        except Exception as e:
            print(f"Error loading data: {e}")
            messagebox.showerror("錯誤", "無法讀取客戶資料")

        self.update_treeview()

    def create_page(self):
        # page Frame
        self.frame_container = tk.Frame(self)
        self.frame_container.pack(fill='both', expand=True)
        # title
        self.title = tk.Label(self.frame_container, text='客戶管理', font=('標楷體', 30, 'bold'), fg='#000000')
        self.title.place(relx=0.5, rely=0.08, relheight=0.1, relwidth=0.5, anchor='center')
        # button - back 
        self.btn_back = tk.Button(self.frame_container, text='回首頁', font=('標楷體', 16, 'bold'), fg='#000000', command=lambda: self.master.change_page(self.master.index_page))
        self.btn_back.place(relx=0.9, rely=0.1, relwidth=0.1, relheight=0.05, anchor='center')
        # treeview 
        self.tree_cms = ttk.Treeview(self.frame_container)
        self.tree_yscroll = tk.Scrollbar(self.tree_cms, orient="vertical")
        self.tree_yscroll.pack(side="right", fill="y")
        self.tree_yscroll.config(command=self.tree_cms.yview) 
        self.tree_cms.configure(yscrollcommand=self.tree_yscroll.set)
        self.tree_cms.place(relx=0.5, rely=0.4, relheight=0.5, relwidth=0.9, anchor='center')
        
        self.tree_cms['columns'] = ('公司名稱', '統編', '公司地址', '聯絡人', '聯絡電話')
        self.tree_cms.column('#0', width=0, stretch=False)  # 隱藏 #0 列
        for column in self.tree_cms['columns']:
            self.tree_cms.heading(column, text=column)
            self.tree_cms.column(column, anchor='center')

        # 綁定點擊事件
        self.tree_cms.bind("<ButtonRelease-1>", self.on_item_selected)
        
        # Entrys Custom
        self.label_custom = tk.Label(self.frame_container, text='公司名稱:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_custom.place(relx=0.15, rely=0.8, relwidth=0.1, relheight=0.05, anchor='center')
        self.entry_custom = tk.Entry(self.frame_container, font=('標楷體', 14, 'bold'))
        self.entry_custom.place(relx=0.32, rely=0.8, relwidth=0.25, relheight=0.04, anchor='center')
        self.label_compiled = tk.Label(self.frame_container, text='統編:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_compiled.place(relx=0.5, rely=0.8, relwidth=0.1, relheight=0.05, anchor='center')
        self.entry_compiled = tk.Entry(self.frame_container, font=('標楷體', 14, 'bold'))
        self.entry_compiled.place(relx=0.67, rely=0.8, relwidth=0.25, relheight=0.04, anchor='center')
        self.label_address = tk.Label(self.frame_container, text='公司地址:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_address.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.05, anchor='center')
        self.entry_address = tk.Entry(self.frame_container, font=('標楷體', 14, 'bold'))
        self.entry_address.place(relx=0.5, rely=0.85, relwidth=0.6, relheight=0.04, anchor='center')
        self.label_contact = tk.Label(self.frame_container, text='聯絡人:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_contact.place(relx=0.15, rely=0.9, relwidth=0.1, relheight=0.05, anchor='center')
        self.entry_contact = tk.Entry(self.frame_container, font=('標楷體', 14, 'bold'))
        self.entry_contact.place(relx=0.32, rely=0.9, relwidth=0.25, relheight=0.04, anchor='center')
        self.label_phone = tk.Label(self.frame_container, text='聯絡電話:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_phone.place(relx=0.5, rely=0.9, relwidth=0.1, relheight=0.05, anchor='center')
        self.entry_phone = tk.Entry(self.frame_container, font=('標楷體', 14, 'bold'))
        self.entry_phone.place(relx=0.67, rely=0.9, relwidth=0.25, relheight=0.04, anchor='center')
        # button - create
        self.btn_create = tk.Button(self.frame_container, text='新增', font=('標楷體', 14, 'bold'), fg='#000000', command=self.create_custom)
        self.btn_create.place(relx=0.8, rely=0.95, relwidth=0.08, relheight=0.04, anchor='center')
        # button - clear
        self.btn_clear = tk.Button(self.frame_container, text='清空', font=('標楷體', 14, 'bold'), fg='#000000', command=self.clear)
        self.btn_clear.place(relx=0.7, rely=0.95, relwidth=0.08, relheight=0.04, anchor='center')
        # button - modify
        self.btn_modify = tk.Button(self.frame_container, text='修改客戶資料', font=('標楷體', 14, 'bold'), fg='#000000', command=self.update_custom)
        self.btn_modify.place(relx=0.3, rely=0.7, relwidth=0.15, relheight=0.04, anchor='center')
        # button - delete
        self.btn_delete = tk.Button(self.frame_container, text='刪除客戶資料', font=('標楷體', 14, 'bold'), fg='#000000', command=self.delete_custom)
        self.btn_delete.place(relx=0.7, rely=0.7, relwidth=0.15, relheight=0.04, anchor='center')

    def update_treeview(self):
        # 先清空現有的內容
        for item in self.tree_cms.get_children():
            self.tree_cms.delete(item)
        
        # 插入資料到 Treeview
        for item in self.cms_datas:
            # print(f"Inserting item: {item}")  # 檢查item的內容是否正確
            self.tree_cms.insert('', 'end', values=item)

    def create_custom(self):
        if self.entry_custom.get()!='' and self.entry_compiled.get()!='' and self.entry_address.get()!='' and self.entry_contact.get()!='' and self.entry_phone.get()!='':
            custom = self.entry_custom.get()
            compiled = self.entry_compiled.get()
            address = self.entry_address.get()
            contact = self.entry_contact.get()
            phone = self.entry_phone.get()
            list_custom = [custom, compiled, address, contact, phone]
            self.excel_cms.create(*list_custom)
            # clear entrys
            self.entry_custom.delete(0, 'end')
            self.entry_compiled.delete(0, 'end')
            self.entry_address.delete(0, 'end')
            self.entry_contact.delete(0, 'end')
            self.entry_phone.delete(0, 'end')
            # update treeview
            self.cms_datas = self.excel_cms.read_all_datas()
            self.update_treeview()
            messagebox.showinfo(title='成功', message='客戶資料已新增')
        else:
            messagebox.showwarning(title='警告', message='客戶資料不能空白')
    
    def clear(self):
        self.entry_custom.delete(0, 'end')
        self.entry_compiled.delete(0, 'end')
        self.entry_address.delete(0, 'end')
        self.entry_contact.delete(0, 'end')
        self.entry_phone.delete(0, 'end')
        self.selected_item_index = None
        self.btn_create.config(state='normal')

    def on_item_selected(self, event):
        # 獲取選中的項目
        selected_item = self.tree_cms.selection()
        self.selected_item_index = self.tree_cms.index(selected_item[0])  # 記錄選中的索引
        if selected_item:
            # 提取選中的值
            item_values = self.tree_cms.item(selected_item, 'values')
            # 將值填入相應的 Entry 控
            self.entry_custom.delete(0, 'end')
            self.entry_custom.insert(0, item_values[0])
            self.entry_compiled.delete(0, 'end')
            self.entry_compiled.insert(0, item_values[1])
            self.entry_address.delete(0, 'end')
            self.entry_address.insert(0, item_values[2])
            self.entry_contact.delete(0, 'end')
            self.entry_contact.insert(0, item_values[3])
            self.entry_phone.delete(0, 'end')
            self.entry_phone.insert(0, item_values[4])
            self.btn_create.config(state='disabled')

    def update_custom(self):
        if self.selected_item_index is not None:
            updated_data = [
                self.entry_custom.get(),
                self.entry_compiled.get(),
                self.entry_address.get(),
                self.entry_contact.get(),
                self.entry_phone.get()
            ]
            # 更新 Excel 中的數據
            self.excel_cms.update_row(self.selected_item_index, updated_data)
            # 更新成功後刷新資料
            self.cms_datas = self.excel_cms.read_all_datas()
            self.update_treeview()
            self.clear()
            messagebox.showinfo(title='成功', message='客戶資料已更新')
        else:
            messagebox.showwarning(title='警告', message='請先選擇一個客戶')

    def delete_custom(self):
        if self.selected_item_index is not None:
            # 確認是否刪除
            confirm = messagebox.askyesno(title='確認', message='確定要刪除這個客戶資料嗎？')
            if confirm:
                # 刪除 Excel 中的資料
                self.excel_cms.delete_row(self.selected_item_index)
                # 刷新資料
                self.cms_datas = self.excel_cms.read_all_datas()
                self.update_treeview()
                self.clear()
                messagebox.showinfo(title='成功', message='客戶資料已刪除')
                self.selected_item_index = None
        else:
            messagebox.showwarning(title='警告', message='請先選擇一個客戶')

class QuotePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # 開啟客戶資料
        try:
            self.excel_cms = ExcelCMS('customers.xlsx')
            self.cms_datas = self.excel_cms.read_all_datas()
            if not self.cms_datas:
                print("Warning: No data found in Excel file.")
        except Exception as e:
            print(f"Error loading data: {e}")
            messagebox.showerror("錯誤", "無法讀取客戶資料")
        self.custom_list = self.excel_cms.get_column_data('A')
        self.unit = ['式', 'L', '組', '顆', '片', '條', '座', '罐', '個', '支']
        self.list_product = []
        self.list_format = []
        self.list_amount = []
        self.list_unit = []
        self.list_cost = []

        self.total_rows = 7
        self.total_height = 50*(self.total_rows+12)

        self.create_page()  # 初始化時創建佈局

    def create_page(self):
        # page Frame
        self.frame_container = ttk.Frame(self)
        self.frame_container.pack(fill='both', expand=True)
        # create canvas
        self.canvas = tk.Canvas(self.frame_container, scrollregion=(0,0,self.frame_container.winfo_width(),self.total_height))
        self.canvas.pack(fill='both', expand=True)
        # frame covered the canvas
        self.inner_frame = ttk.Frame(self.frame_container)
        # self.canvas.create_window((0,0), window=self.inner_frame, anchor='nw', width=self.frame_container.winfo_width(), height=self.frame_container.winfo_height())
        # Scroolbar
        self.scrollbar = ttk.Scrollbar(self.frame_container, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        # canvas event
        self.canvas.bind_all('<MouseWheel>', lambda event:self.canvas.yview_scroll(-int(event.delta/60), 'units'))
        self.frame_container.bind('<Configure>', self.on_frame_configure)

        for x in range(8):
            self.inner_frame.grid_columnconfigure(x, weight=1)  # Allow columns to expand equally
        # Title
        self.title = tk.Label(self.inner_frame, text='報價單', font=('標楷體', 30, 'bold'), fg='#000000')
        self.title.grid(row=0, column=0, columnspan=8, pady=10, padx=10, sticky="nesw")
        # # Buttons
        self.btn_back = tk.Button(self.inner_frame, text='回首頁', font=('標楷體', 16, 'bold'), fg='#000000', command=lambda: self.master.change_page(self.master.index_page))
        self.btn_back.grid(row=1, column=7, pady=10, padx=25, sticky="we")
        self.btn_clear = tk.Button(self.inner_frame, text='清除', font=('標楷體', 16, 'bold'), fg='#000000', command=self.clear)
        self.btn_clear.grid(row=2, column=3, pady=10, padx=10, sticky="we")
        # # Combobox - custom list
        self.lab_custom = tk.Label(self.inner_frame, text='請選擇客戶:', font=('標楷體', 14, 'bold'))
        self.lab_custom.grid(row=2, column=0, pady=5, padx=10, sticky="ew")
        self.combobox_custom = ttk.Combobox(self.inner_frame, values=self.custom_list, font=('標楷體', 14, 'bold'))
        self.combobox_custom.grid(row=2, column=1, columnspan=2, pady=5, padx=10, sticky="ew")
        self.combobox_custom.bind("<<ComboboxSelected>>", self.on_combobox_select)
        # # Entry fields
        self.label_custom = tk.Label(self.inner_frame, text='公司名稱:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_custom.grid(row=3, column=0, pady=5, padx=5, sticky="ew")
        self.entry_custom = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
        self.entry_custom.grid(row=3, column=1, columnspan=2, pady=5, padx=5, sticky="ew")
        self.label_compiled = tk.Label(self.inner_frame, text='統編:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_compiled.grid(row=3, column=3, pady=5, padx=5, sticky="e")
        self.entry_compiled = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
        self.entry_compiled.grid(row=3, column=4, pady=5, padx=10, sticky="w")
        self.label_address = tk.Label(self.inner_frame, text='公司地址:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_address.grid(row=4, column=0, pady=5, padx=10, sticky="ew")
        self.entry_address = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
        self.entry_address.grid(row=4, column=1, columnspan=4, pady=5, padx=5, sticky="ew")
        self.label_contact = tk.Label(self.inner_frame, text='聯絡人:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_contact.grid(row=5, column=0, pady=5, padx=10, sticky="ew")
        self.entry_contact = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
        self.entry_contact.grid(row=5, column=1, columnspan=2, pady=5, padx=10, sticky="ew")
        self.label_phone = tk.Label(self.inner_frame, text='聯絡電話:', font=('標楷體', 14, 'bold'), fg='#000000')
        self.label_phone.grid(row=5, column=3, pady=5, padx=10, sticky="e")
        self.entry_phone = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
        self.entry_phone.grid(row=5, column=4, pady=5, padx=10, sticky="w")
        # Calendar
        # 取得當天日期
        today = datetime.today()
        self.cal = Calendar(self.inner_frame, selectmode="day", year=today.year, month=today.month, day=today.day, date_pattern="yyyy/mm/dd")
        self.cal.grid(row=3, column=5, rowspan=3, sticky="nsew")
        self.label_cal = tk.Label(self.inner_frame, font=('標楷體', 14, 'bold'), text='')
        self.label_cal.grid(row=2, column=5)
        selected_date = self.cal.get_date()
        self.label_cal.config(text="報價日期：" + selected_date)
        # 綁定 <<CalendarSelected>> 事件
        self.cal.bind("<<CalendarSelected>>", self.update_label)
        # # Horizontal Line
        self.h_line = ttk.Separator(self.inner_frame, orient='horizontal')
        self.h_line.grid(row=6, column=0, columnspan=8, pady=10, padx=25, sticky="ew")
        # label subtitle
        self.label_subtitle = tk.Label(self.inner_frame, text="項目列表", font=('標楷體', 18, 'bold'))
        self.label_subtitle.grid(row=7, column=0, columnspan=9, pady=10, sticky='we')
        # 項目列表
        self.label_product = tk.Label(self.inner_frame, text='產品', font=('標楷體', 16, 'bold'))
        self.label_product.grid(row=8, column=0, columnspan=2, padx=25, pady=5, sticky='we')
        self.label_format = tk.Label(self.inner_frame, text='品名/規格', font=('標楷體', 16, 'bold'))
        self.label_format.grid(row=8, column=2, columnspan=2, padx=25, pady=5, sticky='we')
        self.label_amount = tk.Label(self.inner_frame, text='數量', font=('標楷體', 16, 'bold'))
        self.label_amount.grid(row=8, column=4, padx=25, pady=5, sticky='we')
        self.label_unit = tk.Label(self.inner_frame, text='單位', font=('標楷體', 16, 'bold'))
        self.label_unit.grid(row=8, column=5, padx=25, pady=5, sticky='we')
        self.label_cost = tk.Label(self.inner_frame, text='單價', font=('標楷體', 16, 'bold'))
        self.label_cost.grid(row=8, column=6, columnspan=2, padx=25, pady=5, sticky='we')
        # Entrys
        for i in range(self.total_rows):
            self.entry_product = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
            self.entry_product.grid(row=9+i, column=0, columnspan=2, padx=30, pady=5, sticky='we')
            self.list_product.append(self.entry_product)
            self.entry_format = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
            self.entry_format.grid(row=9+i, column=2, columnspan=2, padx=30, pady=5, sticky='we')
            self.list_format.append(self.entry_format)
            self.entry_amount = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
            self.entry_amount.grid(row=9+i, column=4, padx=30, pady=5, sticky='we')
            self.list_amount.append(self.entry_amount)
            self.combobox_unit = ttk.Combobox(self.inner_frame, values=self.unit, font=('標楷體', 14, 'bold'))
            self.combobox_unit.grid(row=9+i, column=5, padx=30, pady=5, sticky='we')
            self.list_unit.append(self.combobox_unit)
            self.entry_cost = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
            self.entry_cost.grid(row=9+i, column=6, columnspan=2, padx=30, pady=5, sticky='we')
            self.list_cost.append(self.entry_cost)
        # button Add
        self.btn_addrow = tk.Button(self.inner_frame, text='+新增', font=('標楷體', 14, 'bold'), command=self.add_row)
        self.btn_addrow.grid(row=self.total_rows+10, column=4, padx=15, pady=10, sticky='we')
        self.btn_confirm = tk.Button(self.inner_frame, text='確認', font=('標楷體', 14, 'bold'), command=self.comfirm)
        self.btn_confirm.grid(row=self.total_rows+11, column=7, padx=30, pady=10, sticky='we')
        
    def update_label(self, event):
        selected_date = self.cal.get_date()  # 取得格式化後的日期
        self.label_cal.config(text="報價日期：" + selected_date)
    
    def add_row(self):
        # Add row entrys
        self.entry_product = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
        self.entry_product.grid(row=9+self.total_rows, column=0, columnspan=2, padx=30, pady=5, sticky='we')
        self.list_product.append(self.entry_product)
        self.entry_format = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
        self.entry_format.grid(row=9+self.total_rows, column=2, columnspan=2, padx=30, pady=5, sticky='we')
        self.list_format.append(self.entry_format)
        self.entry_amount = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
        self.entry_amount.grid(row=9+self.total_rows, column=4, padx=30, pady=5, sticky='we')
        self.list_amount.append(self.entry_amount)
        self.combobox_unit = ttk.Combobox(self.inner_frame, values=self.unit, font=('標楷體', 14, 'bold'))
        self.combobox_unit.grid(row=9+self.total_rows, column=5, padx=30, pady=5, sticky='we')
        self.list_unit.append(self.combobox_unit)
        self.entry_cost = tk.Entry(self.inner_frame, font=('標楷體', 14, 'bold'))
        self.entry_cost.grid(row=9+self.total_rows, column=6, columnspan=2, padx=30, pady=5, sticky='we')
        self.list_cost.append(self.entry_cost)

        self.btn_addrow.grid(row=self.total_rows+10, column=4, padx=15, pady=10, sticky='we')
        self.btn_confirm.grid(row=self.total_rows+11, column=7, padx=30, pady=10, sticky='we')
        # 改變總高度
        self.total_rows += 1
        self.total_height = 40*(self.total_rows+11)
        heights = self.total_height
        # Update the scroll region to encompass the inner frame
        if self.total_height >= self.frame_container.winfo_height():
            heights = self.total_height
            self.canvas.bind_all('<MouseWheel>', lambda event:self.canvas.yview_scroll(-int(event.delta/60), 'units'))
            self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            heights = self.frame_container.winfo_height()
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()
        # 重繪Canvas
        self.canvas.create_window((0,0), window=self.inner_frame, anchor='nw', width=self.frame_container.winfo_width(), height=heights)
        self.canvas.config(scrollregion=self.canvas.bbox("all")) # 重新綁定scrollbar 滾動範圍

    def on_frame_configure(self, event):
        # Update the scroll region to encompass the inner frame
        if self.total_height >= self.frame_container.winfo_height():
            heights = self.total_height
            self.canvas.bind_all('<MouseWheel>', lambda event:self.canvas.yview_scroll(-int(event.delta/60), 'units'))
            self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            heights = self.frame_container.winfo_height()
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()

        self.canvas.create_window((0,0), window=self.inner_frame, anchor='nw', width=self.frame_container.winfo_width(), height=heights)

    def on_combobox_select(self, event):
        selected_value = self.combobox_custom.get()
        selected_index = self.combobox_custom['values'].index(selected_value)
        data = self.excel_cms.get_row_data(selected_index)
        # 修改Entrys
        self.entry_custom.delete(0, 'end')
        self.entry_custom.insert(0, data[0])
        self.entry_compiled.delete(0, 'end')
        self.entry_compiled.insert(0, data[1])
        self.entry_address.delete(0, 'end')
        self.entry_address.insert(0, data[2])
        self.entry_contact.delete(0, 'end')
        self.entry_contact.insert(0, data[3])
        self.entry_phone.delete(0, 'end')
        self.entry_phone.insert(0, data[4])

    def clear(self):
        self.entry_custom.delete(0, 'end')
        self.entry_compiled.delete(0, 'end')
        self.entry_address.delete(0, 'end')
        self.entry_contact.delete(0, 'end')
        self.entry_phone.delete(0, 'end')

    def comfirm(self):
        total_list = []
        product_list = []
        format_list = []
        amount_list = []
        unit_list = []
        cost_list = []

        if self.entry_custom.get() != '':
            custom = self.entry_custom.get()
        else:
            messagebox.showwarning(title='請輸入客戶資料', message='客戶資料不能空白!')
        
        for index, product in enumerate(self.list_product):
            if product.get() != '':
                product_list.append(product.get())
                format_list.append(self.list_format[index].get())
                amount_list.append(self.list_amount[index].get())
                unit_list.append(self.list_unit[index].get())
                cost_list.append(self.list_cost[index].get())

        total_list.append(product_list)
        total_list.append(format_list)
        total_list.append(amount_list)
        total_list.append(unit_list)
        total_list.append(cost_list)

        q_time = self.cal.get_date()
        str_time = q_time.replace('/', '')
        file_name = f'{str_time}_{custom}'
        
        self.excel_quote = ExcelQuote(file_name)
        self.excel_quote.modify_quote(q_time, custom, *total_list)
        # 完整的檔案路徑
        file_path = f'./quote/{file_name}.xlsx'

        if os.path.exists(file_path):
            print(f"要開啟的檔案路徑: {file_path}")  # 確認檔案路徑
            subprocess.Popen(['start', 'excel.exe', file_path], shell=True)
        else:
            print('沒有檔案')
        

        # try:
        #     os.startfile(file_path)
        #     print(f"要開啟的檔案路徑: {file_path}")  # 確認檔案路徑
        # except FileNotFoundError:
        #     print('無法打開指定的文件!')
        # except LookupError:
        #     print('指定了未知的編碼!')
        # except UnicodeDecodeError:
        #     print('讀取文件時解碼錯誤!')
        # except Exception as e:
        #     print(f"無法開啟檔案: {file_path}，錯誤訊息: {e}")
                


class ReportPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_page()  # 初始化時創建佈局

    def create_page(self):
        # page Frame
        self.frame_container = tk.Frame(self)
        self.frame_container.pack(fill='both', expand=True)
        
        # title
        self.title = tk.Label(self.frame_container, text='營收報表', font=('標楷體', 30, 'bold'), fg='#000000')
        self.title.place(relx=0.5, rely=0.1, relheight=0.1, relwidth=0.5, anchor='center')
        
        # buttons
        self.btn_back = tk.Button(self.frame_container, text='回首頁', font=('標楷體', 16, 'bold'), fg='#000000', command=lambda: self.master.change_page(self.master.index_page))
        self.btn_back.place(relx=0.9, rely=0.1, relwidth=0.1, relheight=0.05, anchor='center')


if __name__ == '__main__':
    app = App()
    app.mainloop()
