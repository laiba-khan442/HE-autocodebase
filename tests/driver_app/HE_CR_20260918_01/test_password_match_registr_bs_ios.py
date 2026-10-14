import time
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC


input_password = "123123@789Meshon"
input_confirm_password = "123123@789Meshon"


def test_password_match_registr():
    options = XCUITestOptions().load_capabilities({
        "platformName": "iOS",
        "automationName": "XCUITest",
    })

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    time.sleep(30)

    wait = WebDriverWait(driver, 15)

    # Pre-requisites:
    # The driver should be logged out.
    # A unique email and phone must already be entered.
    # User should be on the create password page before entry of this test case.

    try:
        active_app = driver.execute_script(
            "mobile: activeAppInfo"
        )

        assert active_app["bundleId"] == "com.halaleats.provider"
        print("user is on driver app")

        # Clicks on Get Started button.
        get_started = wait.until(
            EC.visibility_of_element_located((
                AppiumBy.ACCESSIBILITY_ID,
                "Get Started"
            ))
        )

        get_started.click()

        # Assert if the system is on Create Account page.
        create_account = wait.until(
            EC.visibility_of_element_located((
                AppiumBy.ACCESSIBILITY_ID,
                "Create account"
            ))
        )

        assert create_account.is_displayed()

        # Clicks on first-name field and shows keyboard.
        # Android instance(0) becomes XPath index [1] on iOS.
        f_name_input = wait.until(
            EC.visibility_of_element_located((
                AppiumBy.XPATH,
                "(//XCUIElementTypeTextField | "
                "//XCUIElementTypeSecureTextField)[1]"
            ))
        )

        f_name_input.click()

        WebDriverWait(driver, 10).until(
            lambda d: d.is_keyboard_shown()
        )

        assert driver.is_keyboard_shown()

        # Finds the form's scrollable container.
        form_scroll = wait.until(
            EC.presence_of_element_located((
                AppiumBy.CLASS_NAME,
                "XCUIElementTypeScrollView"
            ))
        )

        # Finds Password field on the page.
        # Scroll is restricted to the form so it does not
        # interact with the open iOS keyboard.
        for _ in range(3):
            driver.execute_script(
                "mobile: scroll",
                {
                    "elementId": form_scroll.id,
                    "direction": "down"
                }
            )

        password_field_scroll = driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
            "Password *"
        )

        assert password_field_scroll.is_displayed()

        # Populates Password field.
        # Android instance(2) becomes XPath index [3] on iOS.
        password_field = wait.until(
            EC.visibility_of_element_located((
                AppiumBy.XPATH,
                "(//XCUIElementTypeTextField | "
                "//XCUIElementTypeSecureTextField)[3]"
            ))
        )

        password_field.click()
        password_field.clear()
        password_field.send_keys(input_password)

        # Finds Confirm Password field on the page.
        # Keyboard remains open.
        driver.execute_script(
            "mobile: scroll",
            {
                "elementId": form_scroll.id,
                "direction": "down"
            }
        )

        driver.execute_script(
            "mobile: scroll",
            {
                "elementId": form_scroll.id,
                "name": "Confirm Password *"
            }
        )

        confirm_password_field_scroll = driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
            "Confirm Password *"
        )

        assert confirm_password_field_scroll.is_displayed()

        # Re-enters the same password.
        # The dynamic third-field index remains unchanged.
        confirm_password_field = wait.until(
            EC.visibility_of_element_located((
                AppiumBy.XPATH,
                "(//XCUIElementTypeTextField | "
                "//XCUIElementTypeSecureTextField)[3]"
            ))
        )

        confirm_password_field.click()
        confirm_password_field.clear()
        confirm_password_field.send_keys(
            input_confirm_password
        )

        # Asserts Password Match message.
        success_message = wait.until(
            EC.visibility_of_element_located((
                AppiumBy.ACCESSIBILITY_ID,
                "Password Match"
            ))
        )

        assert success_message.is_displayed()

    finally:
        driver.quit()