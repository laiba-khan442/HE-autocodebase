import re
from xml.etree import ElementTree

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

def open_as_guest():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "automationName": "UiAutomator2",
    })


    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    wait = WebDriverWait(driver, 15)

    try:
        assert driver.current_package == "com.halaleats.user"
        print("user is on homescreen")

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

        # The guest header appears before the General section on the Account page.
        screen = ElementTree.fromstring(driver.page_source)
        labels = [
            value
            for element in screen.iter()
            for attribute in ("text", "content-desc")
            if (value := element.get(attribute))
        ]
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
