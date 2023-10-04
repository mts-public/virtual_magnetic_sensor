import tkinter as tk
from tkinter import ttk


class StatusBar:

    def __init__(self, root: tk.Tk) -> None:

        self.status = ttk.Label(root, text="", relief=tk.GROOVE, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def set(self, message: str) -> None:
        self.status.config(text=message)
