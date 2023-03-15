import tkinter as tk
from tkinter import ttk
from frames.running import RunningFrame
from modules.workers import retrieve_items
from modules.simple_workers import startbot
import asyncio


class BottleOptions(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, padding=(100, 100, 100, 100))
        self.items = retrieve_items()

        self.title = ttk.Label(self, text="Select a bottle")
        self.title.grid(row=0, column=0, columnspan=2)

        self.top = RunningFrame()

        self.combo_box = ttk.Combobox(
            self,
            state="readonly",
        )
        self.combo_box["values"] = self.items
        self.combo_box.grid(row=1, column=0, columnspan=2)

        self.prev_btn = ttk.Button(
            self, text="Prev", command=lambda: controller.show_frame("UserInfo")
        )

        self.run_btn = ttk.Button(self, text="Start Bot", command=self.find)

        self.prev_btn.grid(column=0, row=2, columnspan=1)
        self.run_btn.grid(column=1, row=2, columnspan=1)
        self.status_var = tk.StringVar(self, value="Waiting to Start Watching...")
        self.message_widget = tk.Message(self, textvariable=self.status_var)
        self.message_widget.grid(row=3, column=0, columnspan=2)

    def find(self):
        selected = self.combo_box.get()
        self.status_var.set("Bot is running...")
        self.message_widget.config(textvariable=self.status_var)
        self.message_widget.
        startbot(selected, self.message_widget)
        # if not isinstane(bot, Exception):
        #     self.status.config(text=f"Bot finished!\n Result: {bot}")
