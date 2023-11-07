import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import data_source

class Window(tk.Tk):                     
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #===========更新資料庫資料================#
        try:
            data_source.updata_sqlite_data()
        except Exception:
            messagebox.showerror("錯誤",'網路不正常\n將關閉應用程式\n請稍後再試')
            self.destroy()
        #------------------------------------------

        

    
        #===============主執行程式=================
def main():  
    #print("3",end=" ")  
    def update_data(w:Window)->None:                             
        data_source.updata_sqlite_data()   
        
    window = Window()                             
    window.title('信用卡消費資料')
    window.geometry('600x300')
    window.resizable(width=False,height=False)
    update_data(window)                           #執行程序1-主執行程式
    window.mainloop()

if __name__ == '__main__':
    main()