import logging
import pathlib
import platform
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(
    format="[%(levelname)s] instagram-comments-wipe: %(message)s", level=logging.INFO
)

logging.info("Starting...")
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
    except:
        logging.error(
            "Web driver could not start. Have you installed ChromeDriver? Check README for details"
        )
        sys.exit(1)
    logging.info("Opened Chrome browser")

    # Open Instagram comments page
    driver.get("https://www.instagram.com/your_activity/interactions/comments")
    logging.info(
        "Opening https://www.instagram.com/your_activity/interactions/comments"
    )

    # Sign in & Click 'Not now' on 'Save Your Login Info?' dialog
    while True:
        if driver.current_url.startswith(
            "https://www.instagram.com/your_activity/interactions/comments"
        ):
            logging.info("Login detected")
            break
        try:
            logging.info(
                "Waiting for sign in... (Please go to the browser and sign in. Don't click anything else after signing in!)"
            )
            wait = WebDriverWait(driver, 60)

            def is_not_now_div_present(driver):
                try:
                    div = driver.find_element(By.CSS_SELECTOR, "div[role='button']")
                except:
                    return False
                return div.text == "Not now"

            wait.until(is_not_now_div_present)
            logging.info("Login detected")
            driver.find_element(By.CSS_SELECTOR, "div[role='button']").send_keys(
                Keys.ENTER
            )
            logging.info("Clicked 'Not now' on 'Save Your Login Info?'")
            break
        except TimeoutException:
            pass

    # Main loop
    while True:
        # Click select button
        is_clicked_select = False
        while not is_clicked_select:
            logging.info("Waiting for comments to load...")
            time.sleep(2)
            for i in driver.find_elements(
                By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'
            ):
                if i.text == "Select":
                    for j in driver.find_elements(
                        By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'
                    ):
                        if j.text == "No results":
                            logging.info("No likes found. DONE. Quitting")
                            driver.quit()
                            sys.exit(0)
                    driver.execute_script("arguments[0].click();", i)
                    logging.info("Comments loaded")
                    logging.info("Clicked 'Select'")
                    is_clicked_select = True
                    break
                if i.text == "You haven't commented on anything":
                    logging.info("No likes found. DONE. Quitting")
                    driver.quit()
                    sys.exit(0)

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
                    logging.info(
                        "Selected a comment (Total: " + str(selected_count) + ")"
                    )
            while_it_count += 1
            if while_it_count > 10:
                logging.warning(
                    "Are you seeing this popup -> 'There was a problem with unliking some or all of your content. Try unliking it again.' If so, it looks like you have reached the rate limit for unlike operations. This is a server-side restriction from Instagram. Please wait for a few hours and rerun the script."
                )
                logging.info("Quitting because no further action can be taken for now.")
                driver.quit()
                sys.exit(0)

        # Click delete
        for i in driver.find_elements(
            By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.TextSpan"]'
        ):
            if i.text == "Delete":
                driver.execute_script("arguments[0].click();", i)
                logging.info("Clicked 'Delete'")
                break

        # Confirm delete
        is_clicked_conf_del = False
        while not is_clicked_conf_del:
            time.sleep(1)
            for i in driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] button'):
                if i.find_element(By.CSS_SELECTOR, "div").text == "Delete":
                    driver.execute_script("arguments[0].click();", i)
                    logging.info("Clicked 'Delete' on confirmation dialog")
                    is_clicked_conf_del = True
                    break

except KeyboardInterrupt:
    print()
    logging.info("Quitting on keyboard interrupt...")
    driver.quit()
    sys.exit(0)
except NoSuchWindowException:
    logging.exception("Browser window closed unexpectedly")
    sys.exit(1)
except Exception:
    logging.exception("Unknown error occurred")
    try:
        driver.quit()
    except:
        pass
    sys.exit(1)
