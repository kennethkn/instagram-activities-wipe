import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

print("del-all-ig-comments: Script started")
# while (
#     browser := int(
#         input(
#             "del-all-ig-comments: [1]Chrome [2]Edge [3]Safari. Choose your browser (1/2/3)"
#         )
#     )
# ) not in [1, 2, 3]:
#     pass
browser = 1
try:
    if browser == 3:
        while (
            input(
                "del-all-ig-comments: Go to Safari > Settings... > Developer and check 'Allow Remote Automation' before proceeding. Proceed? (y/n)"
            ).lower()
            != "y"
        ):
            pass
    try:
        driver = (
            webdriver.Chrome()
            if browser == 1
            else (webdriver.Edge() if browser == 2 else webdriver.Safari())
        )
    except Exception as e:
        print(
            e,
            "\ndel-all-ig-comments: Web driver could not start. Have you installed ChromeDriver? Check README for details.",
        )
        raise KeyboardInterrupt
    print(
        "del-all-ig-comments: Opened "
        + ("Chrome" if browser == 1 else ("Edge" if browser == 2 else "Safari"))
        + " browser"
    )
    driver.get("https://www.instagram.com/your_activity/interactions/comments")
    print(
        "del-all-ig-comments: Opening https://www.instagram.com/your_activity/interactions/comments"
    )
    print(
        "del-all-ig-comments: Waiting for sign in... (Please go to the browser and sign in. Don't click anything else after signing in!)"
    )
    # AUTO LOGIN: This code is for auto login which I used extensively during testing, so I'm leaving it here.
    # driver.find_element(By.NAME, "username").send_keys("YOUR_USERNAME")
    # for i in "YOUR_PASSWORD":
    #     driver.find_element(By.NAME, "password").send_keys(i)
    # driver.find_element(By.CSS_SELECTOR, "button[type='submit'] > div").send_keys(
    #     Keys.ENTER
    # )
    # AUTO LOGIN
    while True:
        try:
            wait = WebDriverWait(driver, 60)

            def is_not_now_div_present(driver):
                try:
                    div = driver.find_element(By.CSS_SELECTOR, "div[role='button']")
                except:
                    return False
                return div.text == "Not now"

            wait.until(is_not_now_div_present)
            print("del-all-ig-comments: Login detected.")
            driver.find_element(By.CSS_SELECTOR, "div[role='button']").send_keys(
                Keys.ENTER
            )
            print("del-all-ig-comments: Clicked 'Not now' on 'Save Your Login Info?'")
            break
        except TimeoutException:
            print(
                "del-all-ig-comments: Still waiting for sign in... (Please go to the browser and sign in. Don't click anything else after signing in!)"
            )
    while True:
        comments_wait = WebDriverWait(driver, 30)
        try:
            print("del-all-ig-comments: Looking for comments...")
            comments_wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'div[data-testid="comments_container_non_empty_state"]',
                    )
                )
            )
            print("del-all-ig-comments: Comments loaded")
        except TimeoutException:
            print("del-all-ig-comments: No comments found. DONE")
            raise KeyboardInterrupt
        except Exception as e:
            raise e
        for i in driver.find_elements(
            By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'
        ):
            if i.text == "Select":
                driver.execute_script("arguments[0].click();", i)
                print("del-all-ig-comments: Clicked 'Select'")
                break
        selected_count = 0
        for i in driver.find_elements(
            By.CSS_SELECTOR, 'div[data-bloks-name="ig.components.Icon"]'
        ):
            if i.get_attribute("style").startswith("mask-image:"):
                driver.execute_script("arguments[0].click();", i)
                selected_count += 1
                print(
                    "del-all-ig-comments: Selected a comment for deletion (Total: "
                    + str(selected_count)
                    + ")"
                )
        for i in driver.find_elements(
            By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.TextSpan"]'
        ):
            if i.text == "Delete":
                driver.execute_script("arguments[0].click();", i)
                print("del-all-ig-comments: Clicked 'Delete'")
                break
        for i in driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] button'):
            if i.find_element(By.CSS_SELECTOR, "div").text == "Delete":
                driver.execute_script("arguments[0].click();", i)
                print("del-all-ig-comments: Clicked 'Delete' on confirmation dialog")
                break
except KeyboardInterrupt:
    print("del-all-ig-comments: Quitting...")
except Exception as e:
    print(e)
try:
    driver.quit()
except:
    pass
