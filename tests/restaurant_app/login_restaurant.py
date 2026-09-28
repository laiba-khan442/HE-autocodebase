import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

test_email = "Laiba+origu;oiuoiu@meshon.com.au"
test_password = "12375793579Lk56"

def test_valid_restaurant_login():

    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "TECNO BG7",
        "udid": "108321542O005568",
        "appPackage": "com.halaleats.store",
        "appActivity": ".MainActivity",
        "noReset": True,
    })

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    wait = WebDriverWait(driver, 15)

    try:
        assert driver.current_package == "com.halaleats.store"

        email_input = wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().className("android.widget.EditText").instance(0)'
                )
            )
        )

        password_input = wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().className("android.widget.EditText").instance(1)'
                )
            )
        )
        email_input.click()
        email_input.clear()
        email_input.send_keys(test_email)

        password_input.click()
        password_input.clear()
        password_input.send_keys(test_password)

        login_button = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.ACCESSIBILITY_ID,
                    "Continue to Login"
                )
            )
        )

        login_button.click()


    finally:
        driver.quit()