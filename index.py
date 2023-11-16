import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import data
import pandas as pd
from treeview import TreeView
from concurrent.futures import ThreadPoolExecutor

class Window(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("信用卡消費樣態")

        # -----interface-----#
        #------搜尋------#
        topFrame = ttk.Labelframe(self, text="搜尋")
        self.choose_var = tk.StringVar()
        self.choose_var.set("Select Data")
        self.choose = ttk.Combobox(topFrame, textvariable=self.choose_var, values=["Job", "Incom", "Education", "Sex", "Age"])
        self.choose.grid(row=0, column=0, padx=10, pady=10)
        self.choose.bind("<<ComboboxSelected>>", self.load_data)

        topFrame.pack()

        #------資料呈現------#
        middleFrame = ttk.Labelframe(self, text="資料")
        self.treeview = TreeView(middleFrame,show = 'headings', height = 20)
        self.treeview.grid(row=1, column=0, padx=10, pady=10)
        middleFrame.pack() 
        
        scrollBar = ttk.Scrollbar(middleFrame,orient='vertical',command=self.treeview.yview)
        scrollBar.pack(side='right',fill='y')
        self.treeview.configure(yscrollcommand=scrollBar.set)
       

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
        selected_option = self.choose_var.get()

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

        self.display_data(data)

    def display_data(self, data):
    # 如果數據集不為空
        if not data.empty:
            # 如果前三列的欄位還沒有設定，則設定欄位
            if not hasattr(self, "_columns_set"):
                columns = list(data.columns)[:3]  # 僅取前三列的欄位
                self.treeview["columns"] = columns
                for col in columns:
                    self.treeview.heading(col, text=col, anchor=tk.W)
                    self.treeview.column(col, anchor=tk.W, width=100)

                # 設定 _columns_set，表示前三列的欄位已經設定過
                self._columns_set = True

            # 遍歷數據集，僅取後三列的值，並插入 Treeview
            for index, row in data.iterrows():
                # 取得前三列的值
                values = [row[col] for col in list(data.columns)[:3]]
                item_id = self.treeview.insert("", "end", values=values)

                # 繼續遍歷後三列的值，插入至對應的 item_id 底下
                for col in list(data.columns)[3:]:
                    value = row[col]
                    self.treeview.set(item_id, col, value)

        


def main():
    window = Window()
    window.mainloop()


if __name__ == "__main__":
    main()
