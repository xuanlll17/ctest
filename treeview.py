from tkinter import ttk
import tkinter as tk


class TreeView(ttk.Treeview):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)