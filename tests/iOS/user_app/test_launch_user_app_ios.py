from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.support.ui import WebDriverWait


APP_BUNDLE_ID = "com.halaleats.customer"
FOREGROUND_APP_STATE = 4


def test_launch_user_app_ios():
    options = XCUITestOptions().load_capabilities({
        "platformName": "iOS",
        "automationName": "XCUITest",
        "bundleId": APP_BUNDLE_ID,
        "noReset": True,
    })

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        WebDriverWait(driver, 20).until(
            lambda current_driver: current_driver.query_app_state(APP_BUNDLE_ID)
            == FOREGROUND_APP_STATE
        )
        assert driver.query_app_state(APP_BUNDLE_ID) == FOREGROUND_APP_STATE, (
            "User app is not in the foreground"
        )
    finally:
        driver.quit()
