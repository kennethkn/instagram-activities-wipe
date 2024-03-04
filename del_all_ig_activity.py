import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

print("clear-ig-activity: Script started")
while (
    browser := int(
        input(
            "clear-ig-activity: [1]Chrome [2]Edge [3]Safari. Choose your browser (1/2/3)"
        )
    )
) not in [1, 2, 3]:
    pass
try:
    if browser == 3:
        while (
            input(
                "clear-ig-activity: Go to Safari > Settings... > Developer and check 'Allow Remote Automation' before proceeding. Proceed? (y/n)"
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
            "\nclear-ig-activity: Web driver could not start. Have you installed the appropriate web driver? Check README for more info.",
        )
        raise KeyboardInterrupt
    print(
        "clear-ig-activity: Opened "
        + (
            "Chrome"
            if browser == 1
            else ("Edge" if browser == 2 else "Safari") + " browser"
        )
    )
    driver.get("https://www.instagram.com/your_activity/interactions/comments")
    print(
        "clear-ig-activity: Opening https://www.instagram.com/your_activity/interactions/comments"
    )
    while (
        not input(
            "clear-ig-activity: Sign into your Instagram account before proceeding. Proceed? (y/n)"
        ).lower()
        == "y"
    ):
        pass
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
            div = driver.find_element(By.CSS_SELECTOR, "div[role='button']")
            if div.text == "Not now":
                div.send_keys(Keys.ENTER)
                print("clear-ig-activity: Clicked 'Not now' on 'Save Your Login Info?'")
                break
            else:
                raise Exception
        except:
            print(
                "clear-ig-activity: Expected to see 'Save Your Login Info?' prompt. Retrying in 5 seconds..."
            )
            time.sleep(5)
            print("clear-ig-activity: Retrying now...")
    while True:
        comments_wait = WebDriverWait(driver, 30)
        try:
            print("clear-ig-activity: Looking for comments...")
            comments_wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'div[data-testid="comments_container_non_empty_state"]',
                    )
                )
            )
            print("clear-ig-activity: Comments loaded")
        except TimeoutException:
            print("clear-ig-activity: No comments found. DONE")
            raise KeyboardInterrupt
        except Exception as e:
            raise e
        for i in driver.find_elements(
            By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'
        ):
            if i.text == "Select":
                driver.execute_script("arguments[0].click();", i)
                print("clear-ig-activity: Clicked 'Select'")
                break
        selected_count = 0
        for i in driver.find_elements(
            By.CSS_SELECTOR, 'div[data-bloks-name="ig.components.Icon"]'
        ):
            if i.get_attribute("style").startswith("mask-image:"):
                driver.execute_script("arguments[0].click();", i)
                selected_count += 1
                print(
                    "clear-ig-activity: Selected a comment for deletion (Total: "
                    + str(selected_count)
                    + ")"
                )
        for i in driver.find_elements(
            By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.TextSpan"]'
        ):
            if i.text == "Delete":
                driver.execute_script("arguments[0].click();", i)
                print("clear-ig-activity: Clicked 'Delete'")
                break
        for i in driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] button'):
            if i.find_element(By.CSS_SELECTOR, "div").text == "Delete":
                driver.execute_script("arguments[0].click();", i)
                print("clear-ig-activity: Clicked 'Delete' on confirmation dialog")
                break
except KeyboardInterrupt:
    print("clear-ig-activity: Quitting...")
except Exception as e:
    print(e)
try:
    driver.quit()
except:
    pass
