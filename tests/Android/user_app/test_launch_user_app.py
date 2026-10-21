from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait


APP_PACKAGE = "com.halaleats.user"


def test_launch_user_app():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "TECNO BG7",
        "udid": "108321542O005568",
        "appPackage": APP_PACKAGE,
        "appActivity": "com.halaleats.user.MainActivity",
        "noReset": True,
    })

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        WebDriverWait(driver, 15).until(
            lambda current_driver: current_driver.current_package == APP_PACKAGE
        )
        assert driver.current_package == APP_PACKAGE
    finally:
        driver.quit()
