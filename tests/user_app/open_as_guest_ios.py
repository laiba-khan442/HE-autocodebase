import re
from xml.etree import ElementTree

from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


APP_BUNDLE_ID = "com.halaleats.customer"


def test_open_as_guest_ios():
    options = XCUITestOptions().load_capabilities({
        "platformName": "iOS",
        "automationName": "XCUITest",
    })

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options,
    )
    wait = WebDriverWait(driver, 20)

    try:
        driver.activate_app(APP_BUNDLE_ID)
        assert driver.query_app_state(APP_BUNDLE_ID) == 4, (
            "User app is not in the foreground"
        )

        account_tab = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Account"))
        )
        account_tab.click()

        guest_name = wait.until(
            EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Guest User"))
        )
        assert guest_name.is_displayed()
        assert wait.until(
            EC.visibility_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "Login to view all the features")
            )
        ).is_displayed()

        # iOS exposes visible text through label, name, or value attributes.
        screen = ElementTree.fromstring(driver.page_source)
        labels = []
        for element in screen.iter():
            label = element.get("label") or element.get("name") or element.get("value")
            if label:
                labels.append(label)
        guest_index = labels.index("Guest User")
        general_index = labels.index("General", guest_index + 1)
        header_labels = labels[guest_index:general_index]
        assert not any("@" in label for label in header_labels), (
            "An email address is shown in the guest header"
        )
        assert not any(
            re.search(r"\+?\d(?:[\s().-]*\d){6,}", label)
            for label in header_labels
        ), "A phone number is shown in the guest header"
    finally:
        driver.quit()
