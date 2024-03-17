from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import platform

print("del-all-ig-comments: Script started")
try:
    # Start Chrome browser
    try:
        options = Options()
        # Prevent having to login every time you run the script
        if platform.system() == "Windows":
            options.add_argument(
                "user-data-dir=C:\\Users\\Username\\AppData\\Local\\Google\\Chrome\\User Data"
            )
        else:
            options.add_argument("user-data-dir=/tmp/del-ig-comments-likes")
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(
            e,
            "\ndel-all-ig-comments: Web driver could not start. Have you installed ChromeDriver? Check README for details.",
        )
        raise KeyboardInterrupt
    print("del-all-ig-comments: Opened Chrome browser")

    # Open Instagram comments page
    driver.get("https://www.instagram.com/your_activity/interactions/comments")
    print(
        "del-all-ig-comments: Opening https://www.instagram.com/your_activity/interactions/comments"
    )

    # Sign in & Click 'Not now' on 'Save Your Login Info?' dialog
    while True:
        if driver.current_url.startswith(
            "https://www.instagram.com/your_activity/interactions/comments"
        ):
            print("del-all-ig-comments: Login detected.")
            break
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
                "del-all-ig-comments: Waiting for sign in... (Please go to the browser and sign in. Don't click anything else after signing in!)"
            )

    # Main loop
    while True:
        # Click select button
        is_clicked_select = False
        while not is_clicked_select:
            print("del-all-ig-comments: Waiting for comments to load...")
            time.sleep(2)
            for i in driver.find_elements(
                By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'
            ):
                if i.text == "Select":
                    for j in driver.find_elements(
                        By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'
                    ):
                        if j.text == "No results":
                            print("del-all-ig-comments: No comments found. DONE")
                            raise KeyboardInterrupt
                    driver.execute_script("arguments[0].click();", i)
                    print("del-all-ig-comments: Comments loaded")
                    print("del-all-ig-comments: Clicked 'Select'")
                    is_clicked_select = True
                    break
                if i.text == "You haven't commented on anything":
                    print("del-all-ig-comments: No comments found. DONE")
                    raise KeyboardInterrupt

        # Select all comments
        selected_count = 0
        while_it_count = 0
        while selected_count == 0:
            time.sleep(1)
            for i in driver.find_elements(
                By.CSS_SELECTOR, 'div[data-bloks-name="ig.components.Icon"]'
            ):
                if i.get_attribute("style").startswith(
                    'mask-image: url("https://i.instagram.com/static/images/bloks/icons/generated/circle__outline'
                ):
                    driver.execute_script("arguments[0].click();", i)
                    selected_count += 1
                    print(
                        "del-all-ig-comments: Selected a comment (Total: "
                        + str(selected_count)
                        + ")"
                    )
            while_it_count += 1
            if while_it_count > 20:
                print(
                    "del-all-ig-comments: Are you seeing this popup -> 'There was a problem deleting some or all of your content. Try deleting it again.'"
                )
                print(
                    "del-all-ig-comments: If so, it looks like you have reached the rate limit for comment deletions. This is a server-side restriction from Instagram."
                )
                print(
                    "del-all-ig-comments: Please wait for a few hours and rerun the script."
                )
                time.sleep(100000)
                raise KeyboardInterrupt

        # Click delete
        for i in driver.find_elements(
            By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.TextSpan"]'
        ):
            if i.text == "Delete":
                driver.execute_script("arguments[0].click();", i)
                print("del-all-ig-comments: Clicked 'Delete'")
                break

        # Confirm delete
        is_clicked_conf_del = False
        while not is_clicked_conf_del:
            time.sleep(1)
            for i in driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] button'):
                if i.find_element(By.CSS_SELECTOR, "div").text == "Delete":
                    driver.execute_script("arguments[0].click();", i)
                    print(
                        "del-all-ig-comments: Clicked 'Delete' on confirmation dialog"
                    )
                    is_clicked_conf_del = True
                    break

except KeyboardInterrupt:
    print("del-all-ig-comments: Quitting...")
except Exception as e:
    print(e)
try:
    driver.quit()
except:
    pass
