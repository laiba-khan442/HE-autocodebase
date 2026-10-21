from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


APP_BUNDLE_ID = "com.sixamtech.stackFoodRestaurant"
TEST_EMAIL = "Laiba@meshon.com.au"
TEST_PASSWORD = "123123@Lk56"


def test_valid_restaurant_login_ios():
    options = XCUITestOptions().load_capabilities({
        "platformName": "iOS",
        "automationName": "XCUITest",
    })
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    wait = WebDriverWait(driver, 30)

    # The restaurant app should already be open on its signed-out login screen.
    try:
        active_app = driver.execute_script("mobile: activeAppInfo")
        assert active_app["bundleId"] == APP_BUNDLE_ID, (
            f"Expected restaurant app {APP_BUNDLE_ID}, got {active_app['bundleId']}"
        )

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

        password_input = wait.until(EC.visibility_of_element_located((
            AppiumBy.XPATH, "(//XCUIElementTypeSecureTextField)[1]"
        )))
        password_input.click()
        password_input.clear()
        password_input.send_keys(TEST_PASSWORD)

        if driver.is_keyboard_shown():
            driver.hide_keyboard()

        wait.until(EC.element_to_be_clickable((
            AppiumBy.ACCESSIBILITY_ID, "Login"
        ))).click()

        # The current restaurant dashboard shows this card after owner login.
        dashboard = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((
                AppiumBy.ACCESSIBILITY_ID, "Restaurant availability"
            ))
        )
        assert dashboard.is_displayed()
    finally:
        driver.quit()
