from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


APP_BUNDLE_ID = "com.halaleats.customer"
CARD_NUMBER = "4242424242424242"
EXPIRY_DATE = "0730"
CVC = "123"
CARDHOLDER_NAME = "Laiba Khan"

SAVED_CARD = (
    AppiumBy.IOS_PREDICATE,
    'type == "XCUIElementTypeStaticText" AND '
    '(name CONTAINS "4242" OR label CONTAINS "4242")',
)


def _card_input(driver, label, position):
    """Find a Stripe field by its iOS label, then by its position in CardField."""
    fields = driver.find_elements(
        AppiumBy.XPATH,
        "//XCUIElementTypeTextField | //XCUIElementTypeSecureTextField",
    )
    # Wait for all three native Stripe inputs and the Flutter name input.
    if len(fields) < 4:
        return False
    for field in fields:
        description = " ".join(
            (field.get_attribute(attribute) or "")
            for attribute in ("name", "label", "value")
        ).lower()
        if label in description and field.is_displayed():
            return field

    # CardField is the first form control; the Flutter cardholder field follows it.
    if fields[position].is_displayed():
        return fields[position]
    return False


def _add_card_button(driver):
    for title in ("Add new card", "Add your first card"):
        for button in driver.find_elements(AppiumBy.ACCESSIBILITY_ID, title):
            if button.is_displayed() and button.is_enabled():
                return button
    return False


def test_add_new_card_ios():
    options = XCUITestOptions().load_capabilities({
        "platformName": "iOS",
        "automationName": "XCUITest",
    })
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    wait = WebDriverWait(driver, 20)

    # Pre-requisite: the user is logged in and on the home screen.
    try:
        driver.activate_app(APP_BUNDLE_ID)
        assert driver.query_app_state(APP_BUNDLE_ID) == 4, (
            "User app is not in the foreground"
        )

        account = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Account"))
        )
        account.click()

        payment_method = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, "Payment methods")
            )
        )
        payment_method.click()

        assert wait.until(
            EC.visibility_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "Payment methods")
            )
        ).is_displayed()

        # Record existing cards so a previously saved 4242 card cannot pass the test.
        wait.until(_add_card_button)
        matching_cards_before = len(driver.find_elements(*SAVED_CARD))

        wait.until(_add_card_button).click()
        assert wait.until(
            EC.visibility_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "Add card")
            )
        ).is_displayed()

        # Stripe's iOS CardField contains number, expiry, and CVC inputs.
        card_number = wait.until(lambda d: _card_input(d, "card number", 0))
        card_number.click()
        card_number.send_keys(CARD_NUMBER)

        expiry = wait.until(lambda d: _card_input(d, "expiration", 1))
        expiry.click()
        expiry.send_keys(EXPIRY_DATE)

        cvc = wait.until(lambda d: _card_input(d, "cvc", 2))
        cvc.click()
        cvc.send_keys(CVC)

        cardholder_name = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, "Name on card")
            )
        )
        cardholder_name.click()
        cardholder_name.clear()
        cardholder_name.send_keys(CARDHOLDER_NAME)

        # Dismiss the keyboard so the Save Card button is visible.
        if driver.is_keyboard_shown():
            driver.hide_keyboard()

        save_card = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Save Card"))
        )
        save_card.click()

        # A successful save returns to Payment methods and adds the masked card.
        WebDriverWait(driver, 60).until(
            EC.invisibility_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "Add card")
            )
        )
        assert wait.until(
            EC.visibility_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "Payment methods")
            )
        ).is_displayed()
        wait.until(
            lambda d: len(d.find_elements(*SAVED_CARD)) > matching_cards_before
        )
    finally:
        driver.quit()
