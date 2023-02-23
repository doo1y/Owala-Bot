import json, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()


def list_items():
    items = []
    try:
        driver.get("https://owalalife.com/pages/color-drop")
        elements = driver.find_elements(By.CLASS_NAME, "product__name")
        for i in range(len(elements)):
            items.append(str(elements[i].text))
    except:
        raise Exception("Error Occured \u2639")
    return items


def startbot(session, item):
    try:
        res = session.get("https://owalalife.com/products.json")
        data = json.loads(res.text)
        target = next(x for x in data["products"] if x["title"] == item)
        loop(
            session,
            dict(
                {
                    "handle": target["handle"],
                    "variant_id": target["variants"][0]["id"],
                }
            ),
        )
    except:
        raise Exception


def loop(session, item):
    while True:
        try:
            driver.get(f"https://owalalife.com/products/{item['handle']}")
            button = driver.find_element(
                By.XPATH,
                "//div[@class='color-drop-addcart__product-info']/div[@class='action-button-container']/button",
            )
            if str(button.text) == "Grab bottle":
                checkout(session, item["variant_id"])
        except NoSuchElementException:
            continue
        time.sleep(2)


def checkout(session, variant_id):
    jsonfile = {"items": [{"qualtity": 1, "id": variant_id}], "attributes": {}}
    payload = json.dumps(jsonfile)
    # payload = '{\n\t"items": [\n\t\t{\n\t\t\t"quantity": 1,\n\t\t\t"id": 42859712118943\n\t\t}\n\t],\n\t"attributes": {}\n}'
    headers = {
        "content-type": "application/json;charset=UTF-8",
        "Cookie": "_landing_page=%2Fproducts%2Flucky-you; _orig_referrer=; _s=2bf227e2-ed73-4df5-a8e7-3756f26c4682; _shopify_m=persistent; _shopify_s=2bf227e2-ed73-4df5-a8e7-3756f26c4682; _shopify_tm=; _shopify_tw=; _shopify_y=a144a52d-5bc1-45a7-916f-f2070fa7dbff; _tracking_consent=%7B%22v%22%3A%222.0%22%2C%22lim%22%3A%5B%22GDPR%22%5D%2C%22reg%22%3A%22CCPA%22%2C%22con%22%3A%7B%22GDPR%22%3A%22%22%7D%7D; _y=a144a52d-5bc1-45a7-916f-f2070fa7dbff; cart=36d9abe223c93f20a87abd2469278060; cart_currency=USD; cart_sig=141dedec0b6caf7330b19f3cf16bfa07; cart_ts=1676619783; cart_ver=gcp-us-central1%3A1; localization=US; secure_customer_sig=",
    }
    url = "https://owalalife.com/cart/add.js"
    res = driver.request(
        "POST", url, headers=headers, data=payload, allow_redirects=False
    )
    return res.status_code


def generate_token(card, name, exp_m, exp_yr, cvv):
    """
    Given credit card details, the payment token for a Shopify checkout is
    returned.
    """
    # POST information to get the payment token
    link = "https://elb.deposit.shopifycs.com/sessions"

    payload = {
        "credit_card": {
            "number": card,
            "name": name,
            "month": exp_m,
            "year": exp_yr,
            "verification_value": cvv,
        }
    }
