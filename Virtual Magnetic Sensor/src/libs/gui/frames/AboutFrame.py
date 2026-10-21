import tkinter as tk
from tkinter import ttk
import webbrowser
from typing import Union


class AboutFrame(tk.Toplevel):

    links = [('University of Kaiserslautern-Landau', "https://rptu.de/"),
             ('Institute for Measurement and Sensor Technology', "https://mv.rptu.de/fgs/mts"),
             ('Sensitec GmbH', "https://www.sensitec.com/")]

    def __init__(self, master: Union[tk.Tk, None] = None):
        # toplevel of the main window, so it shares its theme and event loop
        super().__init__(master)
        self.title("Info")
        self.resizable(False, False)

        content = ttk.Frame(self, padding=(24, 20, 24, 16))
        content.pack(fill='both', expand=True)

        ttk.Label(content, text='Virtual Magnetic Sensor', style='Title.TLabel').pack(anchor='w', pady=(0, 12))

        for text, url in self.links:
            label = ttk.Label(content, text=text, style='Link.TLabel', cursor='hand2')
            label.pack(anchor='w', pady=2)
            label.bind("<Button-1>", lambda e, link=url: self.callback(link))

        ttk.Separator(content, orient='horizontal').pack(fill='x', pady=(16, 12))

        ttk.Button(content, text="Ok", width=10, style='Accent.TButton', command=self.ok).pack(side='right')

        self.bind('<Escape>', lambda event: self.ok())
        self.focus_set()

    @staticmethod
    def callback(url):
        webbrowser.open_new(url)

    def ok(self):
        self.destroy()
