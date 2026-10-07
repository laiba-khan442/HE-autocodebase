from appium import webdriver
import time
from appium.options.android import UiAutomator2Options


def test_launch_restaurant_app():
    options = UiAutomator2Options().load_capabilities({
       "platformName": "Android",
       "automationName": "UiAutomator2",
    })

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )
    time.sleep(30)

    try:
        assert driver.current_package == "com.halaleats.store"
        print("Restaurant App launched successfully.")

    finally:
        driver.quit()
