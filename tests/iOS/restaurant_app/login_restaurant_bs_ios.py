from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


TEST_EMAIL = "Laiba@meshon.com.au"
TEST_PASSWORD = "123123@Lk56"


def test_valid_restaurant_login_ios():
    options = XCUITestOptions().load_capabilities({
        "platformName": "iOS",
        "automationName": "XCUITest",
    })
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # BrowserStack reports the bundle ID of the uploaded, installed build.
        app_bundle_id = driver.capabilities.get("bundleId") or driver.capabilities.get(
            "bundleID"
        )
        assert app_bundle_id, "The iOS session did not report an app bundle ID"
        driver.activate_app(app_bundle_id)
        wait.until(
            lambda current_driver: current_driver.execute_script(
                "mobile: activeAppInfo"
            )["bundleId"] == app_bundle_id
        )

        # The restaurant app should now be on its signed-out login screen.
        # The test credentials belong to a restaurant owner.
        wait.until(EC.element_to_be_clickable((
            AppiumBy.ACCESSIBILITY_ID, "Owner Login"
        ))).click()

        email_input = wait.until(EC.visibility_of_element_located((
            AppiumBy.XPATH, "(//XCUIElementTypeTextField)[1]"
        )))
        email_input.click()
        email_input.clear()
        email_input.send_keys(TEST_EMAIL)
        email_focus_id = driver.switch_to.active_element.id

        # WDA cannot dismiss this iPhone keyboard. Tap the password box while
        # it remains open, then verify focus has moved away from the email box.
        email_rect = email_input.rect
        password_labels = driver.find_elements(
            AppiumBy.ACCESSIBILITY_ID, "Password"
        )
        if password_labels:
            label_rect = password_labels[0].rect
            password_y = (
                label_rect["y"] + label_rect["height"]
                + email_rect["height"] / 2
            )
        else:
            password_y = email_rect["y"] + email_rect["height"] * 2.2
        driver.execute_script("mobile: tap", {
            "x": email_rect["x"] + email_rect["width"] / 2,
            "y": password_y,
        })

        def focused_password(d):
            active = d.switch_to.active_element
            return active if active.id != email_focus_id else False

        password_input = wait.until(
            focused_password,
            "Password field did not receive focus after tapping it",
        )
        password_input.send_keys(TEST_PASSWORD)

        wait.until(EC.element_to_be_clickable((
            AppiumBy.ACCESSIBILITY_ID, "Continue to Login"
        ))).click()

        # Dashboard wording differs between the uploaded app and current source.
        dashboard = WebDriverWait(driver, 60).until(lambda d: next(
            (element for title in ("Restaurant Status", "Restaurant availability")
             for element in d.find_elements(AppiumBy.ACCESSIBILITY_ID, title)
             if element.is_displayed()),
            False,
        ))
        assert dashboard.is_displayed()
    finally:
        driver.quit()
