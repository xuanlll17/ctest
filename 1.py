import tkinter as tk
from tkinter import ttk
import pandas as pd

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer")

        # 下拉選單
        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Select Data")
        self.dropdown = ttk.Combobox(root, textvariable=self.dropdown_var, values=["Job", "Incom", "Education"])
        self.dropdown.grid(row=0, column=0, padx=10, pady=10)
        self.dropdown.bind("<<ComboboxSelected>>", self.load_data)

        # 文本框
        self.textbox = tk.Text(root, height=20, width=50)
        self.textbox.grid(row=1, column=0, padx=10, pady=10)

    def load_data(self, event):
        selected_option = self.dropdown_var.get()

        if selected_option == "Job":
            data = pd.read_csv("job.csv")  # 替換為你的 job CSV 檔案名稱
        elif selected_option == "Incom":
            data = pd.read_csv("incom.csv")  # 替換為你的 income CSV 檔案名稱
        elif selected_option == "Education":
            data = pd.read_csv("education.csv")  # 替換為你的 education CSV 檔案名稱
        else:
            data = pd.DataFrame()

        self.display_data(data)

    def display_data(self, data):
        self.textbox.delete(1.0, tk.END)  # 清空文本框

        if not data.empty:
            self.textbox.insert(tk.END, data)

def main():
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
