import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import data


class Window(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("信用卡消費樣態")
        # -----interface-----#
        topFrame = ttk.Labelframe(self, text="搜尋")
        tk.Label(topFrame, text="").pack()
        topFrame.pack()

        middleFrame = ttk.Labelframe(self, text="主圖")
        tk.Label(middleFrame, text="").pack()
        middleFrame.pack()

        bottomFrame1 = ttk.Labelframe(self, text="副圖1")
        tk.Label(bottomFrame1, text="").pack()
        bottomFrame1.pack()

        bottomFrame2 = ttk.Labelframe(self, text="副圖2")
        tk.Label(bottomFrame2, text="").pack()
        bottomFrame2.pack()

        bottomFrame3 = ttk.Labelframe(self, text="副圖3")
        tk.Label(bottomFrame3, text="").pack()
        bottomFrame3.pack()


def main():
    window = Window()
    window.mainloop()


if __name__ == "__main__":
    main()
