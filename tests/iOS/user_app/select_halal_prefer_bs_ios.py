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


    # Manual preparation window:
    # Grant permissions, complete onboarding/login,
    # and navigate to the home screen.

    driver.execute_script(
        'browserstack_executor: {'
        '"action":"updateIosDeviceSettings",'
        '"arguments":{"LocationServices":"ON"}}'
    )

    driver.terminate_app("com.halaleats.customer")
    driver.activate_app("com.halaleats.customer")

    time.sleep(60)

    wait = WebDriverWait(driver, 20)

    try:

        # Confirm the home screen and open Account.
        nav_account = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID,
                "Account"
            ))
        )

        assert nav_account.is_displayed()
        print("User is on the home screen.")

        nav_account.click()

        # Scroll down to Halal preference.
        driver.execute_script(
            "mobile: scroll",
            {"name": "Halal preference"}
        )

        halal_preference_navigation = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID,
                "Halal preference"
            ))
        )

        halal_preference_navigation.click()

        # Confirm that the preference screen opened.
        preference_heading = wait.until(
            EC.visibility_of_element_located((
                AppiumBy.ACCESSIBILITY_ID,
                "Select Your Halal Preference"
            ))
        )

        assert preference_heading.is_displayed()
        print("Halal preference screen opened.")

        # Select Fully Halal Certified.
        fully_certified = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.IOS_PREDICATE,
                'name == "Fully Halal Certified" OR '
                'label == "Fully Halal Certified"'
            ))
        )

        fully_certified.click()

        # The iOS screen shows Continue, not Save.
        continue_button = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.IOS_PREDICATE,
                'type == "XCUIElementTypeButton" AND '
                '(name CONTAINS "Continue" OR label CONTAINS "Continue")'
            ))
        )

        continue_button.click()

        # Capture the short confirmation message.
        confirmation = WebDriverWait(
            driver,
            5,
            poll_frequency=0.1
        ).until(
            EC.presence_of_element_located((
                AppiumBy.ACCESSIBILITY_ID,
                "Halal preference saved"
            ))
        )

        assert confirmation.is_displayed()
        print("Halal preference saved successfully.")

    finally:
        driver.quit()