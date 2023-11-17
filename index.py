import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import data
import pandas as pd
from treeview import TreeView


class Window(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("信用卡消費樣態")

        # -----interface-----#
        #------搜尋------#
        topFrame = ttk.Labelframe(self, text="搜尋")
        self.data_var = tk.StringVar()
        self.data_var.set("資料類別")
        self.data = ttk.Combobox(topFrame, textvariable=self.data_var, values=["Job", "Incom", "Education", "Sex", "Age"])
        self.data.grid(row=0, column=0, padx=10, pady=10)
        self.data.bind("<<ComboboxSelected>>", self.load_data)

        self.year_var = tk.StringVar()
        self.year_var.set("年分")
        self.year = ttk.Combobox(topFrame, textvariable = self.year_var, values = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'])
        self.year.grid(row=0, column=1, padx=10, pady=10)

        topFrame.pack()

        #------資料呈現------#
        middleFrame = ttk.Labelframe(self, text="資料")
        self.treeview = TreeView(middleFrame, show='headings', height=20)
        self.treeview.grid(row=1, column=0, padx=10, pady=10)

        # 垂直滾動條
        scrollBar = ttk.Scrollbar(middleFrame, orient='vertical', command=self.treeview.yview)
        scrollBar.grid(row=1, column=1, sticky='ns')  # 使用 grid 進行佈局管理

        self.treeview.configure(yscrollcommand=scrollBar.set)

        middleFrame.pack()

       

        #------分析------#
        bottomFrame1 = ttk.Labelframe(self, text="圖1")
        tk.Label(bottomFrame1, text="").pack()
        bottomFrame1.pack()

        bottomFrame2 = ttk.Labelframe(self, text="圖2")
        tk.Label(bottomFrame2, text="").pack()
        bottomFrame2.pack()

        bottomFrame3 = ttk.Labelframe(self, text="圖3")
        tk.Label(bottomFrame3, text="").pack()
        bottomFrame3.pack()
        
    def load_data(self, event):
        selected_option = self.data_var.get()

        if selected_option == "Job":
            data = pd.read_csv("job.csv")
        elif selected_option == "Incom":
            data = pd.read_csv("incom.csv")
        elif selected_option == "Education":
            data = pd.read_csv("education.csv")
        elif selected_option == "Sex":
            data = pd.read_csv("sex.csv")
        elif selected_option == "Age":
            data = pd.read_csv("age.csv")

            years = data['年'].unique()
            self.year['values'] = ['Select Year'] + list(map(int, years))
            select.year_var.set("Select Year")

        selected_year = self.year_var.get()
        if selected_year != "Select Year":
            data = data[data['年'] == int(selected_year)] 

        self.display_data(data)

    def display_data(self, data):
        self.treeview.delete(*self.treeview.get_children())  # 清空 Treeview

        if not data.empty:
            columns = list(data.columns)
            self.treeview["columns"] = columns
            for col in columns:
                self.treeview.heading(col, text=col, anchor='w')
                self.treeview.column(col, anchor='w', width=100)  # 設定欄位寬度，可以自行調整

            for index, row in data.iterrows():
                values = [row[col] for col in columns]
                self.treeview.insert("", "end", values=values)

        


def main():
    window = Window()
    window.mainloop()


if __name__ == "__main__":
    main()
