from tkinter import ttk, font


class GreetUser(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        main_title = font.Font(
            family="Helvetica", name="appMainTitleFont", size=24, weight="bold"
        )

        self.label = ttk.Label(self, text="Owala Bot", font=main_title)
        self.label.grid(row=0, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.button = ttk.Button(
            self, text="Start", command=lambda: controller.show_frame("UserInfo")
        )
        self.button.grid(row=1, sticky="n")
