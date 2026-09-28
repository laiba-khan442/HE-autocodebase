from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC


def test_launch_user_app():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "TECNO BG7",
        "udid": "108321542O005568",
        "appPackage": "com.halaleats.user",
        "appActivity": "com.halaleats.user.MainActivity",
        "noReset": True,
    })


    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    wait = WebDriverWait(driver, 15)

    try:
# runs a while loop until the if conditions is met, otherwise performs the elif block.
        while  != driver.current_package == "com.halaleats.user":
               if driver.current_package == "com.halaleats.user":
                    lang = wait.until(
                         EC.visibility_of_element_located(
                             (
                                 AppiumBy.ACCESSIBILITY_ID,
                                 'English'
                             )
                         ))
                    lang.click()

                    next_screen = wait.until(
                         EC.visibility_of_element_located(
                             (
                                 AppiumBy.ACCESSIBILITY_ID,
                                 'Next'
                             )
                         ))
                    next_screen.click()

                    skip_intro = wait.until(
                         EC.visibility_of_element_located(
                             (
                                 AppiumBy.ACCESSIBILITY_ID,
                                 'Skip'
                             )
                         ))
                    skip_intro.click()

                    assert driver.current_package == "com.halaleats.user"
                    print("User App launched successfully.")



               elif driver.current_package == "com.google.android.permissioncontroller":
                    assert driver.current_package == "com.google.android.permissioncontroller"
                    allow_notif = wait.until(
                          EC.visibility_of_element_located(
                              (
                                  AppiumBy.ANDROID_UIAUTOMATOR,
                                  'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_button")'
                              )
                          ))
                    allow_notif.click()
    finally:
        driver.quit()
