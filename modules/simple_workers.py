import json, time, requests, random, urllib3
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotInteractableException,
    ElementNotSelectableException,
)
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
    frame_to_be_available_and_switch_to_it,
)
from urllib3.exceptions import InsecureRequestWarning

options = Options()
options.headless = False

driver = webdriver.Chrome()

urllib3.disable_warnings(InsecureRequestWarning)

data = {"url": "https://owalalife.com"}

timeout = 1


def check_availability():
    while True:
        try:
            driver.get(f"{data['url']}/products/{data['handle']}")
            driver.find_element(
                By.XPATH,
                "//div[@class='color-drop-addcart__product-info']/div[@class='action-button-container']/button['Grab bottle']",
            )
            return True
        except NoSuchElementException as unreleased:

            time.sleep(timeout)


def fill_checkout_options(status):
    checkout_options = [
        ("checkout_email", data["email"]),
        ("checkout_shipping_address_first_name", data["fname"]),
        ("checkout_shipping_address_last_name", data["lname"]),
        ("checkout_shipping_address_address1", data["addr"]),
        ("checkout_shipping_address_address2", data["addr2"]),
        ("checkout_shipping_address_city", data["city"]),
        ("checkout_shipping_address_zip", data["zip"]),
        ("checkout_shipping_address_phone", data["phone"]),
        ("checkout_shipping_address_country", data["country"]),
        ("checkout_shipping_address_province", data["state"]),
    ]

    for idx, (id, value) in enumerate(checkout_options):
        element = driver.find_element(By.ID, id)
        if element.tag_name == "input":
            element.send_keys(value)
            if id == "checkout_email":
                try:
                    time.sleep(1.5)
                    wait = WebDriverWait(driver, timeout=4)
                    wait.until(
                        frame_to_be_available_and_switch_to_it(
                            (By.CLASS_NAME, "sp-modal__frame")
                        )
                    )
                    time.sleep(1.5)
                    element = driver.find_element(
                        By.CSS_SELECTOR, "[aria-label='Close']"
                    )
                    element.click()
                except ElementNotInteractableException as e:
                    time.sleep(1.5)
                    wait = WebDriverWait(driver, timeout=4)
                    wait.until(
                        frame_to_be_available_and_switch_to_it(
                            (By.CLASS_NAME, "sp-modal__frame")
                        )
                    )
                    time.sleep(1.5)
                    element = driver.find_element(
                        By.CSS_SELECTOR, "[aria-label='Close']"
                    )
                    element.click()
                except Exception as e:
                    print(e)
        elif element.tag_name == "select":
            select_element = Select(element)
            select_element.select_by_value(value)
        status.config(text=f"{id}: {value}")
        driver.switch_to.default_content()
        time.sleep(0.2)

    driver.find_element(By.ID, "continue_button").click()
    WebDriverWait(driver, timeout=1).until(
        lambda x: x.find_element(By.CLASS_NAME, "input-radio").is_selected()
    )
    driver.find_element(By.ID, "continue_button").click()


def fill_checkout_and_pay(status):
    try:
        card_details = [
            ("number", data["card"]),
            ("name", data["fname"] + " " + data["lname"]),
            ("expiry", data["exp_m"] + data["exp_yr"]),
            ("verification_value", data["cvc"]),
        ]

        iframes = driver.find_elements(By.CLASS_NAME, "card-fields-iframe")
        time.sleep(1)
        for idx, iframe in enumerate(iframes):
            time.sleep(1)
            driver.switch_to.frame(
                driver.find_element(By.ID, iframe.get_attribute("id"))
            )
            time.sleep(1)
            wait = WebDriverWait(driver, timeout=3)
            wait.until(element_to_be_clickable((By.ID, card_details[idx][0])))
            time.sleep(1)
            status.config(text=f"{card_details[idx]}")
            if card_details[idx][0] == "expiry":
                for i in card_details[idx][1]:
                    driver.find_element(By.ID, "expiry").send_keys(i)
                    time.sleep(0.1)
            else:
                driver.execute_script(
                    f"""
                    const input = document.querySelector('#{card_details[idx][0]}');
                    input.value = "{card_details[idx][1]}";
                    """
                )
            time.sleep(1)
            driver.switch_to.parent_frame()
            # id = iframe.get_attribute("id").split("-")[2]
            # WebDriverWait(driver, 20).until(
            #     element_to_be_clickable(
            #         (
            #             By.ID,
            #             id,
            #         )
            #     )
            # )
            # element = driver.find_element(By.ID, id)
            # element.click()
            # element.send_keys(card_details[id])
        return True
    except Exception as e:
        status.config(text=e)


def checkout():
    driver.find_element(By.ID, "continue_button").click()


def startbot(item, status):
    try:
        # Grab the products database from the site and filter out the items
        res = requests.get(f"{data['url']}/products.json")
        resBody = json.loads(res.text)
        target = next(x for x in resBody["products"] if x["title"] == item)
        data["var_id"] = str(target["variants"][0]["id"])
        data["handle"] = target["handle"]

        status.config(text=f"Waiting for {item} to drop...")
        available = check_availability()
        if available:
            status.config(text=f"{item} dropped!")
            driver.get(f"{data['url']}/cart/{data['var_id']}:1")

            status.config(text="Filling out shipping information...")
            fill_checkout_options(status)

            status.config(text="Shipping Form Complete! Moving On...")
            time.sleep(3)

            status.config(text="Filling Out Payment Information...")
            fill_checkout_and_pay(status)

            status.config(text="Finishing up checkout process...")
            checkout()

            status.config(
                text=f"All Task Complete! \n Order details: {driver.current_url}"
            )

    except Exception as e:
        status.config(text=e)
        return driver


# USE driver.get(f"https://owalalife.com/cart/{resBody['products'][2]['variants'][0]['id']}:1") AS TEST LINK
