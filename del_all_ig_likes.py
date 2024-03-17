from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import platform
import pathlib

print("del-all-ig-likes: Script started")
try:
    # Start Chrome browser
    try:
        options = Options()
        # Store login in a Chrome profile
        if platform.system() == "Windows":
            wd = pathlib.Path().absolute()
            options.add_argument(f"user-data-dir={wd}\\chrome-profile")
        else:
            options.add_argument("user-data-dir=chrome-profile")
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(
            e,
            "\ndel-all-ig-likes: Web driver could not start. Have you installed ChromeDriver? Check README for details.",
        )
        raise KeyboardInterrupt
    print("del-all-ig-likes: Opened Chrome browser")

    # Open Instagram likes page
    driver.get("https://www.instagram.com/your_activity/interactions/likes")
    print(
        "del-all-ig-likes: Opening https://www.instagram.com/your_activity/interactions/likes"
    )

    # Sign in & Click 'Not now' on 'Save Your Login Info?' dialog
    while True:
        if driver.current_url.startswith(
            "https://www.instagram.com/your_activity/interactions/likes"
        ):
            print("del-all-ig-likes: Login detected.")
            break
        try:
            print(
                "del-all-ig-likes: Waiting for sign in... (Please go to the browser and sign in. Don't click anything else after signing in!)"
            )
            wait = WebDriverWait(driver, 60)

            def is_not_now_div_present(driver):
                try:
                    div = driver.find_element(By.CSS_SELECTOR, "div[role='button']")
                except:
                    return False
                return div.text == "Not now"

            wait.until(is_not_now_div_present)
            print("del-all-ig-likes: Login detected.")
            driver.find_element(By.CSS_SELECTOR, "div[role='button']").send_keys(
                Keys.ENTER
            )
            print("del-all-ig-likes: Clicked 'Not now' on 'Save Your Login Info?'")
            break
        except TimeoutException:
            pass

    # Main loop
    while True:
        # Click select button
        is_clicked_select = False
        while not is_clicked_select:
            print("del-all-ig-likes: Waiting for likes to load...")
            time.sleep(2)
            for i in driver.find_elements(
                By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'
            ):
                if i.text == "Select":
                    for j in driver.find_elements(
                        By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'
                    ):
                        if j.text == "No results":
                            print("del-all-ig-likes: No likes found. DONE")
                            raise KeyboardInterrupt
                    driver.execute_script("arguments[0].click();", i)
                    print("del-all-ig-likes: Likes loaded")
                    print("del-all-ig-likes: Clicked 'Select'")
                    is_clicked_select = True
                    break
                if i.text == "You haven't liked anything":
                    print("del-all-ig-likes: No likes found. DONE")
                    raise KeyboardInterrupt

        # Select all posts
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
                        "del-all-ig-likes: Selected a post (Total: "
                        + str(selected_count)
                        + ")"
                    )
            while_it_count += 1
            if while_it_count > 10:
                print(
                    "del-all-ig-likes: Are you seeing this popup -> 'There was a problem with unliking some or all of your content. Try unliking it again.'"
                )
                print(
                    "del-all-ig-likes: If so, it looks like you have reached the rate limit for unlike operations. This is a server-side restriction from Instagram."
                )
                print(
                    "del-all-ig-likes: Please wait for a few hours and rerun the script."
                )
                raise KeyboardInterrupt

        # Click unlike
        for i in driver.find_elements(
            By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.TextSpan"]'
        ):
            if i.text == "Unlike":
                driver.execute_script("arguments[0].click();", i)
                print("del-all-ig-likes: Clicked 'Unlike'")
                break

        # Confirm unlike
        is_clicked_conf_unlike = False
        while not is_clicked_conf_unlike:
            time.sleep(1)
            for i in driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] button'):
                if i.find_element(By.CSS_SELECTOR, "div").text == "Unlike":
                    driver.execute_script("arguments[0].click();", i)
                    print("del-all-ig-likes: Clicked 'Unlike' on confirmation dialog")
                    is_clicked_conf_unlike = True
                    break

except KeyboardInterrupt:
    print("del-all-ig-likes: Quitting...")
except Exception as e:
    print(e)
try:
    driver.quit()
except:
    pass
