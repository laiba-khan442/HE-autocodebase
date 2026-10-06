from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

password = "123123@789Meshon"
re-enter_password = "123123@789Meshon"

def test_password_match_registr():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "TECNO BG7",
        "udid": "108321542O005568",
        "appPackage": "com.halaleats.provider",
        "appActivity": "com.halaleats.driver.MainActivity",
        "noReset": True,
    })


    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

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
                     'Get Started'
                 )
             ))
       get_started.click()

# assert if the system is on create account page

       create_account = wait.until(
             EC.visibility_of_element_located(
                 (
                     AppiumBy.ACCESSIBILITY_ID,
                     'Create account'
                 )
             )
         )

       assert create_account.is_displayed()

# clicks on the password field and enters test data 