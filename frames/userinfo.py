import json, re, datetime
import tkinter as tk
from tkinter import ttk
from modules.simple_workers import data


# Start App
class UserInfo(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.entry_dict = {
            "Canada": [
                "Alberta AB",
                "British Columbia BC",
                "Manitoba MB",
                "New Brunswick NB",
                "Newfoundland and Labrador NL",
                "Nova Scotia NS",
                "Northwest Territories NT",
                "Nunavut NU",
                "Ontario  ON",
                "Prince Edward Island PE",
                "Quebec QC",
                "Saskatchewan SK",
                "Yukon YT",
            ],
            "United States": [
                "Alabama AL",
                "Alaska AK",
                "Arizona AZ",
                "Arkansas AR",
                "California CA",
                "Colorado CO",
                "Connecticut CT",
                "Delaware DE",
                "Florida FL",
                "Georgia GA",
                "Hawaii HI",
                "Idaho ID",
                "Illinois IL",
                "Indiana IN",
                "Iowa IA",
                "Kansas KS",
                "Kentucky KY",
                "Louisiana LA",
                "Maine ME",
                "Maryland MD",
                "Massachusetts MA",
                "Michigan MI",
                "Minnesota MN",
                "Mississippi MS",
                "Missouri MO",
                "Montana MT",
                "Nebraska NE",
                "Nevada NV",
                "New Hampshire NH",
                "New Jersey NJ",
                "New Mexico NM",
                "New York NY",
                "North Carolina NC",
                "North Dakota ND",
                "Ohio OH",
                "Oklahoma OK",
                "Oregon OR",
                "Pennsylvania PA",
                "Rhode Island RI",
                "South Carolina SC",
                "South Dakota SD",
                "Tennessee TN",
                "Texas TX",
                "Utah UT",
                "Vermont VT",
                "Virginia VA",
                "Washington WA",
                "West Virginia WV",
                "Wisconsin WI",
                "Wyoming WY",
            ],
        }

        self.country_var = tk.StringVar(self)
        self.state_var = tk.StringVar(self)
        self.country_var.trace("w", self.update)

        self.title = ttk.Label(self, text="Please Provide The Following Information")
        self.title.grid(column=0, row=0, columnspan=2)

        self.email_label = ttk.Label(self, text="Email: ")
        self.phone_label = ttk.Label(self, text="Phone: ")
        self.fname_label = ttk.Label(self, text="First Name: ")
        self.lname_label = ttk.Label(self, text="Last Name: ")
        self.addr_label = ttk.Label(self, text="Address: ")
        self.addr2_label = ttk.Label(self, text="Address 2 (Optional): ")
        self.country_label = ttk.Label(self, text="Country: ")
        self.state_label = ttk.Label(self, text="State: ")
        self.city_label = ttk.Label(self, text="City: ")
        self.zip_label = ttk.Label(self, text="Zip: ")
        self.card_label = ttk.Label(self, text="Card Number: ")
        self.month_label = ttk.Label(self, text="Exp Month: ")
        self.yr_label = ttk.Label(self, text="Exp Year: ")
        self.cvc_label = ttk.Label(self, text="CVC: ")

        self.email_entry = ttk.Entry(self)
        self.phone_entry = ttk.Entry(self)
        self.fname_entry = ttk.Entry(self)
        self.lname_entry = ttk.Entry(self)
        self.addr_entry = ttk.Entry(self)
        self.addr2_entry = ttk.Entry(self)
        self.country_entry = tk.OptionMenu(
            self, self.country_var, *self.entry_dict.keys()
        )
        self.state_entry = tk.OptionMenu(self, self.state_var, "")
        self.country_var.set("United States")
        self.city_entry = ttk.Entry(self)
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
        self.grid()

        prev_btn = ttk.Button(
            self, text="Prev", command=lambda: controller.show_frame("GreetUser")
        )

        next_btn = ttk.Button(
            self, text="Next", command=lambda: self.set_obj(controller)
        )
        prev_btn.grid(column=0, columnspan=1, row=15)
        next_btn.grid(column=1, columnspan=1, row=15)

    def update(self, *args):
        countries = self.entry_dict[self.country_var.get()]
        self.state_var.set(countries[0])

        menu = self.state_entry["menu"]
        menu.delete(0, "end")

        for country in countries:
            menu.add_command(
                label=country, command=lambda nation=country: self.state_var.set(nation)
            )

    def set_obj(self, controller):
        user_data = {
            "email": self.email_entry.get(),
            "phone": self.phone_entry.get(),
            "fname": self.fname_entry.get(),
            "lname": self.lname_entry.get(),
            "addr": self.addr_entry.get(),
            "addr2": self.addr2_entry.get(),
            "country": self.country_var.get(),
            "city": self.city_entry.get(),
            "state": self.state_var.get().split(" ")[-1],
            "zip": self.zip_entry.get(),
            "card": self.card_entry.get(),
            "exp_m": self.month_entry.get(),
            "exp_yr": self.yr_entry.get(),
            "cvc": self.cvc_entry.get(),
        }
        for id in user_data:
            if not len(user_data[id]) and id != "addr2":
                pass
            else:
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
