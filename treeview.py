from tkinter import ttk
import tkinter as tk
from tkinter.simpledialog import Dialog


class TreeView(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent  # 加'self.' -> 實體(attribute) #整個class的任何地方都可以用

        # ------bind button1------#
        self.bind("<ButtonRelease-1>", self.selectedItem)

    def selectedItem(self, event):
        selectedItem = self.focus()
        data_dict = self.item(selectedItem)
        data_list = data_dict["values"]
        detail = ShowDetail(self.parent, data=data_list, title="資訊")


class ShowDetail(Dialog):
    def __init__(self, parent, data, **kwargs):
        self.site = data[1]
        self.county = data[2]
        self.pm25 = data[3]
        self.datacreationdate = data[4]
        
        super().__init__(parent, **kwargs)

    def body(self, master):
        """
        override body
        """
        mainFrame = tk.Frame(master)
        mainFrame.pack(padx=100, pady=100)

        heading = TreeView['heading']
        values = [TreeView['values']]


    def buttonbox(self):
        """
        override buttonbox
        """
        box = tk.Frame(self)
        w = tk.Button(box, text="確認", width=10, command=self.ok, default="active")
        w.pack(padx=5, pady=(5, 20))
        self.bind("<Return>", self.ok)

        box.pack()
