import json, re, datetime
import tkinter as tk
from tkinter import ttk
from modules.workers import data

# Start App
class UserInfo(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.label_choice = "State: "
        n = self.label_choice
        self.title = ttk.Label(
            self, text="Please Provide The Following Information For Payment Processing"
        )
        self.title.grid(column=0, row=0, columnspan=2)
        self.email_label = ttk.Label(self, text="Email: ")
        self.phone_label = ttk.Label(self, text="Phone: ")
        self.fname_label = ttk.Label(self, text="First Name: ")
        self.lname_label = ttk.Label(self, text="Last Name: ")
        self.addr_label = ttk.Label(self, text="Address: ")
        self.addr2_label = ttk.Label(self, text="Address 2 (Optional): ")
        self.country_label = ttk.Label(self, text="Country: ")
        self.state_label = ttk.Label(self, text=n)
        self.city_label = ttk.Label(self, text="City: ")
        self.zip_label = ttk.Label(self, text="Zip: ")
        self.card_label = ttk.Label(self, text="Card Number: ")
        self.month_label = ttk.Label(self, text="Exp Month: ")
        self.yr_label = ttk.Label(self, text="Exp Year: ")
        self.cvc_label = ttk.Label(self, text="CVC: ")

        self.entry_choice = [
            "Alaska",
            "Alabama",
            "Arkansas",
            "Arizona",
            "California",
            "Colorado",
            "Connecticut",
            "District of Columbia",
            "Delaware",
            "Florida",
            "Georgia",
            "Hawaii",
            "Iowa",
            "Idaho",
            "Illinois",
            "Indiana",
            "Kansas",
            "Kentucky",
            "Louisiana",
            "Massachusetts",
            "Maryland",
            "Maine",
            "Michigan",
            "Minnesota",
            "Missouri",
            "Mississippi",
            "Montana",
            "North Carolina",
            "North Dakota",
            "Nebraska",
            "New Hampshire",
            "New Jersey",
            "New Mexico",
            "Nevada",
            "New York",
            "Ohio",
            "Oklahoma",
            "Oregon",
            "Pennsylvania",
            "Rhode Island",
            "South Carolina",
            "South Dakota",
            "Tennessee",
            "Texas",
            "Utah",
            "Virginia",
            "Vermont",
            "Washington",
            "Wisconsin",
            "West Virginia",
            "Wyoming",
        ]
        v = self.entry_choice
        self.email_entry = ttk.Entry(self)
        self.phone_entry = ttk.Entry(self)
        self.fname_entry = ttk.Entry(self)
        self.lname_entry = ttk.Entry(self)
        self.addr_entry = ttk.Entry(self)
        self.addr2_entry = ttk.Entry(self)
        self.country_entry = ttk.Combobox(self, values=("United States", "Canada"))
        self.country_entry.bind("<<ComboboxSelected>>", self.fill)
        self.country_entry.current(0)
        self.city_entry = ttk.Entry(self)
        self.state_entry = ttk.Combobox(self, values=v)
        self.zip_entry = ttk.Entry(self)
        self.card_entry = ttk.Entry(self)
        self.month_entry = ttk.Entry(self)
        self.yr_entry = ttk.Entry(self)
        self.cvc_entry = ttk.Entry(self)

        self.email_label.grid(column=0, row=1)
        self.phone_label.grid(column=0, row=2)
        self.fname_label.grid(column=0, row=3)
        self.lname_label.grid(column=0, row=4)
        self.addr_label.grid(column=0, row=5)
        self.addr2_label.grid(column=0, row=6)
        self.country_label.grid(column=0, row=7)
        self.state_label.grid(column=0, row=8)
        self.city_label.grid(column=0, row=9)
        self.zip_label.grid(column=0, row=10)
        self.card_label.grid(column=0, row=11)
        self.month_label.grid(column=0, row=12)
        self.yr_label.grid(column=0, row=13)
        self.cvc_label.grid(column=0, row=14)

        self.email_entry.grid(column=1, row=1)
        self.phone_entry.grid(column=1, row=2)
        self.fname_entry.grid(column=1, row=3)
        self.lname_entry.grid(column=1, row=4)
        self.addr_entry.grid(column=1, row=5)
        self.addr2_entry.grid(column=1, row=6)
        self.country_entry.grid(column=1, row=7)
        self.state_entry.grid(column=1, row=8)
        self.city_entry.grid(column=1, row=9)
        self.zip_entry.grid(column=1, row=10)
        self.card_entry.grid(column=1, row=11)
        self.month_entry.grid(column=1, row=12)
        self.yr_entry.grid(column=1, row=13)
        self.cvc_entry.grid(column=1, row=14)

        prev_btn = ttk.Button(
            self, text="Prev", command=lambda: controller.show_frame("GreetUser")
        )

        next_btn = ttk.Button(
            self, text="Next", command=lambda: self.set_obj(controller)
        )
        prev_btn.grid(column=0, columnspan=1, row=15)
        next_btn.grid(column=1, columnspan=1, row=15)

    def fill(self):
        n = "Province: " if self.country_entry.get() == "Canada" else self.label_choice
        v = (
            [
                "Alberta",
                "British Columbia",
                "Manitoba",
                "New Brunswick",
                "Newfoundland and Labrador",
                "Nova Scotia",
                "Northwest Territories",
                "Nunavut",
                "Ontario",
                "Prince Edward Island",
                "Quebec",
                "Saskatchewan",
                "Yukon",
            ]
            if self.country_entry.get() == "Canada"
            else self.entry_choice
        )
        self.state_label.config(text=n)
        self.state_entry.config(values=v)
        self.state_entry.current(0)

    def set_obj(self, controller):
        user_data = {
            "email": self.email_entry.get(),
            "phone": self.phone_entry.get(),
            "fname": self.fname_entry.get(),
            "lname": self.lname_entry.get(),
            "addr": self.addr_entry.get(),
            "addr2": self.addr2_entry.get(),
            "country": self.country_entry.get(),
            "city": self.city_entry.get(),
            "state": self.state_entry.get(),
            "zip": self.zip_entry.get(),
            "card": self.card_entry.get(),
            "exp_m": self.month_entry.get(),
            "exp_yr": self.yr_entry.get(),
            "cvc": self.cvc_entry.get(),
        }
        data.update(user_data)
        controller.show_frame("BottleOptions")


# TODO : impliment appropriate validations ttk.Entry(s)
# Validator Functions
# def val_email(input) -> bool:
#     """Email validation"""
#     regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
#     if re.fullmatch(regex, input):
#         return True

#     return False


# def val_(input) -> bool:
#     """General non-empty string validation"""
#     return len(input) != 0


# def val_card(input) -> bool:
#     """Credit card validation"""
#     card = [int(x) for x in input]
#     total = card.pop(-1)
#     for i in range(0, len(card), 2):
#         if i != 0:
#             total += card[i - 1]
#         card[i] = card[i] * 2
#         card[i] = card[i] - 9 if card[i] > 9 else card[i]
#         total += card[i]
#     return total % 10 == 0


# def val_month(input) -> bool:
#     """Exp month validation"""
#     return 1 <= int(input) <= 12 and isinstance(int(input), int)


# def val_year(input) -> bool:
#     """Exp year validation"""
#     return int(input) >= datetime.datetime.now().year and isinstance(int(input), int)


# def val_cvc(input) -> bool:
#     """CVC number validation"""
#     return 3 <= len(input) <= 4 and isinstance(int(input), int)
