import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
from tkinter.simpledialog import Dialog

class Window(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("信用卡消費樣態")
        self.conn = sqlite3.connect("creditcard.db")

        # -----------interface-----------#
        mainFrame = tk.Frame(self, relief=tk.GROOVE, borderwidth=1)
        tk.Label(mainFrame, text='信用卡消費樣態', font=('arial', 20), fg='#333333', padx=10, pady=10).pack(padx=20, pady=20, fill='both')
        mainFrame.pack(padx=30, pady=10, fill='both')

        # ------搜尋------#
        topFrame = ttk.Labelframe(self, text="搜尋")
        # -------Label------#
        self.dataLabel = ttk.Label(topFrame, text="資料類別:").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.yearLabel = ttk.Label(topFrame, text="年份:").grid(
            row=0, column=2, padx=10, pady=10
        )
        self.monthLabel = ttk.Label(topFrame, text="月份:").grid(
            row=0, column=4, padx=10, pady=10
        )
        self.areaLabel = ttk.Label(topFrame, text="地區:").grid(
            row=0, column=6, padx=10, pady=10
        )
        self.industryLabel = ttk.Label(topFrame, text="產業別:").grid(
            row=0, column=8, padx=10, pady=10
        )
        # ------StringVar------#
        self.data_var = tk.StringVar()
        self.data_var.set("Select Data")
        self.data = ttk.Combobox(
            topFrame,
            textvariable=self.data_var,
            values=["job", "incom", "education", "sex", "age"],
        )
        self.data.grid(row=0, column=1, padx=10, pady=10)
        self.data.bind("<<ComboboxSelected>>", self.load_data)

        self.year_var = tk.StringVar()
        self.year_var.set("Select Year")
        self.year = ttk.Combobox(
            topFrame,
            textvariable=self.year_var,
            values=[
                "2014",
                "2015",
                "2016",
                "2017",
                "2018",
                "2019",
                "2020",
                "2021",
                "2022",
                "2023",
            ],
        )
        self.year.grid(row=0, column=3, padx=10, pady=10)
        self.year.bind("<<ComboboxSelected>>", self.load_year)

        self.month_var = tk.StringVar()
        self.month_var.set("Select Month")
        self.month = ttk.Combobox(
            topFrame,
            textvariable=self.month_var,
            values=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "ALL"
            ],
        )
        self.month.grid(row=0, column=5, padx=10, pady=10)
        self.month.bind("<<ComboboxSelected>>", self.load_month)

        self.area_var = tk.StringVar()
        self.area_var.set("Select Area")
        self.area = ttk.Combobox(
            topFrame,
            textvariable=self.area_var,
            values=[
                "臺北市",
                "高雄市",
                "新北市",
                "臺中市",
                "臺南市",
                "桃園市",
                "宜蘭縣",
                "新竹縣",
                "苗栗縣",
                "彰化縣",
                "南投縣",
                "雲林縣",
                "嘉義縣",
                "嘉義市",
                "屏東縣",
                "臺東縣",
                "花蓮縣",
                "澎湖縣",
                "基隆市",
                "新竹市",
                "金門縣",
                "連江縣",
                "ALL"
            ],
        )
        self.area.grid(row=0, column=7, padx=10, pady=10)
        self.area.bind("<<ComboboxSelected>>", self.load_area)

        self.industry_var = tk.StringVar()
        self.industry_var.set("Select Industry")
        self.industry = ttk.Combobox(
            topFrame,
            textvariable=self.industry_var,
            values=["食", "衣", "住", "行", "文教康樂", "百貨", "其他", "ALL"],
        )
        self.industry.grid(row=0, column=9, padx=10, pady=10)
        self.industry.bind("<<ComboboxSelected>>", self.load_industry)

        topFrame.pack(padx=30, pady=10, fill='both')

        # ------------資料呈現------------#
        middleFrame = ttk.Labelframe(self, text="資料")
        self.treeview = ttk.Treeview(middleFrame, show="headings", height=20)
        self.treeview.grid(row=1, column=0, padx=10, pady=10)

        # -----垂直滾動條------#
        scrollBar = ttk.Scrollbar(
            middleFrame, orient="vertical", command=self.treeview.yview
        )
        scrollBar.grid(row=1, column=1, sticky="ns")  # 使用 grid 進行佈局管理

        self.treeview.configure(yscrollcommand=scrollBar.set)

        middleFrame.pack()

        # ------------分析------------#
        bottomFrame1 = ttk.Labelframe(self, text="圖1")
        tk.Label(bottomFrame1, text="").pack()
        bottomFrame1.pack()

        bottomFrame2 = ttk.Labelframe(self, text="圖2")
        tk.Label(bottomFrame2, text="").pack()
        bottomFrame2.pack()

        bottomFrame3 = ttk.Labelframe(self, text="圖3")
        tk.Label(bottomFrame3, text="").pack()
        bottomFrame3.pack()

        # Bind the event after creating self.treeview
        self.treeview.bind("<ButtonRelease-1>", self.selectedItem)

    def load_data(self, event):
        self.load_treeview()

    def load_year(self, event):
        self.load_treeview()

    def load_month(self, event):
        self.load_treeview()

    def load_area(self, event):
        self.load_treeview()

    def load_industry(self, event):
        self.load_treeview()

    def load_treeview(self):
        selected_option = self.data_var.get()
        selected_year = self.year_var.get()
        selected_month = self.month_var.get()
        selected_area = self.area_var.get()
        selected_industry = self.industry_var.get()

        if selected_option and selected_year:
            sql = f"SELECT * FROM {selected_option} WHERE 年 = '{selected_year}'"

            if selected_month and selected_month != "Select Month" and selected_month != "ALL":
                sql += f" AND 月 = '{selected_month}'"

            if selected_area and selected_area != "Select Area" and selected_area != "ALL":
                sql += f" AND 地區 = '{selected_area}'"

            if selected_industry and selected_industry != "Select Industry" and selected_industry != "ALL":
                sql += f" AND 產業別 = '{selected_industry}'"

            data = pd.read_sql_query(sql, self.conn)
            self.display_data(data)


    def selectedItem(self, event):
        selected_item = self.treeview.focus()
        data_dict = self.treeview.item(selected_item)
        data_list = data_dict["values"]
        if data_list:
            index = self.treeview.index(selected_item)
             # 將欄位名稱和資料一起傳遞給 ShowDetail
            ShowDetail(self, self.treeview['columns'], data_list, title="資訊")

    def display_data(self, data):
        self.treeview.delete(*self.treeview.get_children())  # 清空 Treeview

        if not data.empty:
            columns = list(data.columns)
            self.treeview["columns"] = columns
            for col in columns:
                self.treeview.heading(col, text=col, anchor="w")
                self.treeview.column(col, anchor="w", width=100)  # 設定欄位寬度，可以自行調整

            for index, row in data.iterrows():
                values = [row[col] for col in columns]
                self.treeview.insert("", "end", values=values)

class ShowDetail(Dialog):
    def __init__(self, parent, columns, data, **kwargs):
        self.columns = columns
        self.data = data
        super().__init__(parent, **kwargs)

    def body(self, master):

        try:
            for col, value in zip(self.columns, self.data):
                dataInfo = tk.Label(master, text=f"{col}:  {value}")
                dataInfo.pack(pady=1, anchor='nw')
        except Exception as e:
            print(f"Exception in ShowDetail: {e}")
            print("Columns:", self.columns)
            print("Data:", self.data)

    def buttonbox(self):
        box = tk.Frame(self)
        w = tk.Button(box, text="確認", width=10, command=self.ok, default="active")
        w.pack(padx=5, pady=(5, 20))
        self.bind("<Return>", self.ok)

        box.pack()



def main():
    window = Window()
    window.resizable(width=False,height=False)
    window.mainloop()


if __name__ == "__main__":
    main()