# from seleniumrequests import Chrome
# from selenium.webdriver.chrome.options import Options
import requests, json

# options = Options()

# options.headless = True

# driver = Chrome(options=options)

link = "https://elb.deposit.shopifycs.com/sessions"

payload = {
    "credit_card": {
        "number": "1234123412341234",
        "name": "FNAME LNAME",
        "month": "12",
        "year": "2025",
        "verification_value": "177",
    }
}

# res = driver.request("POST", link, json=payload)

res = requests.post(link, json=payload)
print(json.loads(res.text)["id"])
print(res)
