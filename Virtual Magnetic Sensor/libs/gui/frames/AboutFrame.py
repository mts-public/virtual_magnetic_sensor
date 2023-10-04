import tkinter as tk
from tkinter import ttk
import webbrowser


class AboutFrame(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Info")

        ttk.Label(self, text='Virtual Magnetic Sensor', font=("Arial", 16)).pack()

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        rptu_label = ttk.Label(self, text='University of Kaiserslautern-Landau', font=("Arial", 11))
        rptu_label.pack(anchor='w')
        rptu_label.bind("<Button-1>", lambda e: self.callback("https://rptu.de/"))

        mts_label = ttk.Label(self, text='Institute for Measurement and Sensor Technology', font=("Arial", 11))
        mts_label.pack(anchor='w')
        mts_label.bind("<Button-1>", lambda e: self.callback("https://mv.rptu.de/fgs/mts"))

        sensitec_label = ttk.Label(self, text='Sensitec GmbH', font=("Arial", 11))
        sensitec_label.pack(anchor='w')
        sensitec_label.bind("<Button-1>", lambda e: self.callback("https://www.sensitec.com/"))

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        ttk.Button(self, text="Ok", command=self.ok).pack(side='bottom')

        self.mainloop()

    @staticmethod
    def callback(url):
        webbrowser.open_new(url)

    def ok(self):
        self.destroy()
        self.quit()
