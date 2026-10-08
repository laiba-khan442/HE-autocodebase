import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

input_password = "123123@789Meshon"
input_confirm_password = "123123@Meshon"

def test_password_match_registr():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "automationName": "UiAutomator2",
        })


    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    time.sleep(30)

    wait = WebDriverWait(driver, 15)

# Pre-requisites:
# The driver should be logged out.
# A unique email and phone must already be entered
# User should be on the create password page before entry of this test case.

    try:
        assert driver.current_package == "com.halaleats.provider"
        print("user is on driver app")

# clicks on get started button
        get_started = wait.until(
        EC.visibility_of_element_located(
         (
             AppiumBy.ACCESSIBILITY_ID,
             "Get Started"
         ))
        )
        get_started.click()


# assert if the system is on create account page

        create_account = wait.until(
        EC.visibility_of_element_located(
         (
             AppiumBy.ACCESSIBILITY_ID,
             'Create account'
         ))
        )
        assert create_account.is_displayed()

# Clicks on first_name field and shows keyboard.
        f_name_input = wait.until(
        EC.visibility_of_element_located(
         (
             AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().className("android.widget.EditText").instance(0)'
         ))
        )
        f_name_input.click()

        WebDriverWait(driver, 10).until(lambda d: d.is_keyboard_shown())

        assert driver.is_keyboard_shown()

# Finds password field on the page
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.setAsVerticalList()'
            '.scrollToEnd(3)'
        )

        password_field_scroll = driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
                'Password *'
        )

        assert password_field_scroll.is_displayed()

# Populates password field.

        password_field = wait.until(
        EC.visibility_of_element_located(
            (
            AppiumBy. ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").instance(1)'
            )
        )
        )
        password_field.click()
        password_field.clear()
        password_field.send_keys(input_password)

# Finds confirm password field on the page
        confirm_password_field_scroll = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.setAsVerticalList()'
            '.scrollForward()'
            '.scrollIntoView(new UiSelector().description("Confirm Password *"))'
        )

        assert confirm_password_field_scroll.is_displayed()

# Re-enters the same password

        confirm_password_field = wait.until(
        EC.visibility_of_element_located(
            (
            AppiumBy. ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").instance(1)'
            )
        )
        )
        confirm_password_field.click()
        confirm_password_field.clear()
        confirm_password_field.send_keys(input_confirm_password)

# Asserts "Password doesn't Match" message is shown
        negative_success_message = wait.until(
                EC.visibility_of_element_located(
                 (
                     AppiumBy.ACCESSIBILITY_ID,
                     "Password doesn't match"
                 ))
                )
        assert negative_success_message.is_displayed()


    finally:
        driver.quit()