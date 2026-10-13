import time

from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_select_halal_pref():
    options = XCUITestOptions().load_capabilities({
        "platformName": "iOS",
        "automationName": "XCUITest",
    })

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    try:
        wait = WebDriverWait(driver, 30)

        # Temporary time for manually preparing the precondition:
        # User is logged in and positioned on the home screen.
        time.sleep(60)

        # Confirm home screen and open Account.
        nav_account = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID,
                "Account"
            ))
        )

        assert nav_account.is_displayed()
        print("User is on the home screen.")

        nav_account.click()

        # Scroll to Halal Preference using an iOS command.
        driver.execute_script(
            "mobile: scroll",
            {"name": "Halal preference"}
        )

        halal_pref_nav = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID,
                "Halal preference"
            ))
        )

        halal_pref_nav.click()

        # Confirm preference screen.
        halal_pref_section = wait.until(
            EC.visibility_of_element_located((
                AppiumBy.ACCESSIBILITY_ID,
                "Select Your Halal Preference"
            ))
        )

        assert halal_pref_section.is_displayed()

        # Replace this value with the exact accessibility ID
        # displayed in Appium Inspector for the iOS element.
        fully_certified = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID,
                "Fully halal-certified"
            ))
        )

        fully_certified.click()

        save_preference = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID,
                "Save"
            ))
        )

        save_preference.click()

        # Verify confirmation.
        confirmation = WebDriverWait(
            driver,
            5,
            poll_frequency=0.2
        ).until(
            EC.visibility_of_element_located((
                AppiumBy.ACCESSIBILITY_ID,
                "Halal preference saved"
            ))
        )

        assert confirmation.is_displayed()
        print("Halal preference saved successfully.")

    finally:
        driver.quit()