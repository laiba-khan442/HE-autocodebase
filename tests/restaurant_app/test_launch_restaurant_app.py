from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_launch_restaurant_app():
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

    try:
        assert driver.current_package == "com.halaleats.store"
        print("Restaurant App launched successfully.")

    finally:
        driver.quit()
