import time
import tkinter as tk
from tkinter import ttk


class RunningFrame(tk.Toplevel):
    def __init__(self, parent=None):
        tk.Toplevel.__init__(self, parent)
        self.finished = True
        self.geometry("430x450")
        self.withdraw()
        self.text = "Bot is Listening"
        self.label = ttk.Label(self, text=self.text)
        self.label.grid()
        while not self.finished:
            for i in range(0, 5):
                self.text = self.text + "."
                self.label.config(text=self.text)
                time.sleep(0.5)
            self.text = "Bot is Listening"

    def stop_bot(self):
        self.finished = True
        self.text = "Purchase Completed!"
        self.label.config(text=self.text)
        self.button = ttk.Button(self, text="Close Bot", command=self.quit)
        self.button.grid()

    def display(self):
        self.wm_deiconify()
        self.finished = False
