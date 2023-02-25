import tkinter as tk
from tkinter import ttk
from tkinter import font
from frames.bottleoptions import BottleOptions
from frames.greetuser import GreetUser
from frames.userinfo import UserInfo


class AppContainer(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self):

        # __init__ function for class Tk
        tk.Tk.__init__(self)

        frm = ttk.Frame(self, padding=10)  # instantiate a child container
        frm.grid()

        frm.grid_rowconfigure(0, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        # dict that will hold the pages
        self.frames = {}

        for fr in (GreetUser, UserInfo, BottleOptions):

            # initialize each frame as children of 'frm' and store it by their name
            page_name = fr.__name__
            frame = fr(parent=frm, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = frame

        self.show_frame("GreetUser")

    # 'controller' method to display frame by next/prev buttons
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
