import json, time, requests, random, urllib3
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

options = Options()
options.headless = True

driver = webdriver.Chrome(
    service=ChromiumService(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    ),
    options=options,
)

session = requests.session()

urllib3.disable_warnings(InsecureRequestWarning)

data = {"url": "https://owalalife.com"}

timeout = 1


def check_availability():
    while True:
        try:
            driver.get(f"https://owalalife.com/products/{data['handle']}")
            driver.find_element(
                By.XPATH,
                "//div[@class='color-drop-addcart__product-info']/div[@class='action-button-container']/button['Grab bottle']",
            )
            return True
        except:
            time.sleep(timeout)
            pass


def retrieve_items():
    items = []
    try:
        driver.get(f"{data['url']}/pages/color-drop")
        elements = driver.find_elements(By.CLASS_NAME, "product__name")
        for i in range(len(elements)):
            items.append(str(elements[i].text))
        return items
    except:
        raise Exception("Error Occured \u2639")


def fetch_cart():
    data["cart_route"] = f"https://owalalife.com/cart/{data['var_id']}:1"


def generate_token():
    route = "https://elb.deposit.shopifycs.com/sessions"

    payload = {
        "credit_card": {
            "number": data["card"],
            "name": data["fname"] + data["lname"],
            "month": data["exp_m"],
            "year": data["exp_yr"],
            "verification_value": data["cvc"],
        }
    }

    res = requests.post(route, json=payload, verify=False)
    return json.loads(res.text)["id"]


def submit_customer_info(cookies):
    """
    Given a session and cookies for a Shopify checkout, the customer's info
    is submitted.
    """
    # Submit the customer info
    payload = {
        "utf8": "\u2713",
        "_method": "patch",
        "authenticity_token": "",
        "previous_step": "contact_information",
        "step": "shipping_method",
        "checkout[email]": data["email"],
        "checkout[buyer_accepts_marketing]": "0",
        "checkout[shipping_address][first_name]": data["fname"],
        "checkout[shipping_address][last_name]": data["lname"],
        "checkout[shipping_address][company]": "",
        "checkout[shipping_address][address1]": data["addr"],
        "checkout[shipping_address][address2]": data["addr2"],
        "checkout[shipping_address][city]": data["city"],
        "checkout[shipping_address][country]": data["country"],
        "checkout[shipping_address][province]": data["state"],
        "checkout[shipping_address][zip]": data["zip"],
        "checkout[shipping_address][phone]": data["phone"],
        "checkout[remember_me]": "0",
        "checkout[client_details][browser_width]": "1710",
        "checkout[client_details][browser_height]": "1289",
        "checkout[client_details][javascript_enabled]": "1",
        "button": "",
    }

    route = data["url"] + "//checkout.json"
    res = session.get(route, cookies=cookies, verify=False)

    # Get the checkout URL
    res_route = res.url

    # POST the data to the checkout URL
    res = session.post(res_route, cookies=cookies, data=payload, verify=False)

    # Return the response and the checkout link
    return res_route


def get_shipping_token(cookies):
    """
    Fetches and constructs a shopify shipping token and returns the token
    """
    # Get the shipping rate info from the Shopify site
    route = f"{data['url']}//cart/shipping_rates.json?shipping_address[zip]={data['zip']}&shipping_address[country]={data['country']}&shipping_address[province]={data['state']}"
    r = session.get(route, cookies=cookies, verify=False)

    # Load the shipping options
    shipping_options = json.loads(r.text)

    # Select the first shipping option
    ship_opt = shipping_options["shipping_rates"][0]["name"].replace(" ", "%20")
    ship_prc = shipping_options["shipping_rates"][0]["price"]

    # Generate the shipping token to submit with checkout
    data["shipping_token"] = f"shopify-{ship_opt}-{ship_prc}"


def get_checkout_gateway(checkout_route, cookies):

    """
    With the provided checkout url and the cookies, retrieves the payment gateway ID
    """

    r = session.get(
        f"{checkout_route}?step=payment_method", cookies=cookies, verify=False
    )

    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find("div", {"class": "radio__input"})
    values = str(div.input).split('"')  # type: ignore
    for value in values:
        if value.isnumeric():
            data["gateway"] = value
            break


def make_purchase(checkout_route, cookies):
    payload = {
        "utf8": "\u2713",
        "_method": "patch",
        "authenticity_token": "",
        "previous_step": "payment_method",
        "step": "",
        "s": data["token"],
        "checkout[payment_gateway]": data["gateway"],
        "checkout[credit_card][vault]": "false",
        "checkout[different_billing_address]": "true",
        "checkout[billing_address][first_name]": data["fname"],
        "checkout[billing_address][last_name]": data["lname"],
        "checkout[billing_address][address1]": data["addr"],
        "checkout[billing_address][address2]": data["addr2"],
        "checkout[billing_address][city]": data["city"],
        "checkout[billing_address][country]": data["country"],
        "checkout[billing_address][province]": data["state"],
        "checkout[billing_address][zip]": data["zip"],
        "checkout[billing_address][phone]": data["phone"],
        "checkout[shipping_rate][id]": data["shipping_token"],
        "complete": "1",
        "checkout[client_details][browser_width]": str(random.randint(1000, 2000)),
        "checkout[client_details][browser_height]": str(random.randint(1000, 2000)),
        "checkout[client_details][javascript_enabled]": "1",
        "g-recaptcha-repsonse": "",
        "button": "",
    }

    r = session.post(checkout_route, cookies=cookies, data=payload, verify=False)
    return r


def startbot(item):
    try:

        res = session.get("https://owalalife.com/products.json")
        resbody = json.loads(res.text)
        target = next(x for x in resbody["products"] if x["title"] == item)
        data["var_id"] = str(target["variants"][0]["id"])
        data["handle"] = target["handle"]
        data["token"] = generate_token()
        available = check_availability()
        if available == True:
            fetch_cart()
            cart_res = session.get(
                f"{data['url']}/cart/add.js?quantity=1&id={data['var_id']}",
                verify=False,
            )
            checkout_route = submit_customer_info(cart_res.cookies)
            get_shipping_token(cart_res.cookies)
            get_checkout_gateway(
                checkout_route=checkout_route, cookies=cart_res.cookies
            )
            r = make_purchase(checkout_route=checkout_route, cookies=cart_res.cookies)
            return r.status_code
    except Exception as e:
        return e
