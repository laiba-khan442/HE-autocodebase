from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

card_num = "4242424242424242"
exp_date = "07/30"
cvc = "123"
name = "Laiba Khan"

def test_add_new_card():
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

# pre-requisite: user should be logged in and should be on the home page.

    try:
        assert driver.current_package == "com.halaleats.user"
        print("user is on homescreen")

        # clicks on account

        nav_account = wait.until(
             EC.visibility_of_element_located(
                 (
                     AppiumBy.ACCESSIBILITY_ID,
                     'Account'
                 )
             ))
        nav_account.click()

        account_section = wait.until(
              EC.element_to_be_clickable(
                  (AppiumBy.ANDROID_UIAUTOMATOR,
                      'new UiSelector().description("Account").instance(1)'
                  )
              )
          )

        assert account_section.is_displayed()

        # navigates payment method section

        payment_method = wait.until(
             EC.visibility_of_element_located(
                 (
                     AppiumBy.ACCESSIBILITY_ID,
                     'Payment Method'
                 )
             ))
        payment_method.click()

        payment_method_sect = wait.until(
              EC.element_to_be_clickable(
                  (AppiumBy.ACCESSIBILITY_ID,
                      'Payment methods'
                  )
              )
          )
        assert payment_method_sect.is_displayed()

            # clicks on add new card

        add_card = wait.until(
             EC.visibility_of_element_located(
                 (
                     AppiumBy.ACCESSIBILITY_ID,
                     'Add new card'
                 )
             ))
        add_card.click()

        add_card_sect = wait.until(
              EC.element_to_be_clickable(
                  (AppiumBy.ACCESSIBILITY_ID,
                      'Add card'
                  )
              )
          )
        assert add_card_sect.is_displayed()

            # adds card details

        add_card_num = wait.until(
             EC.visibility_of_element_located(
                 (
                     AppiumBy.ANDROID_UIAUTOMATOR,
                     'new UiSelector().resourceId("com.halaleats.user:id/card_number_edit_text")'
                 )
             ))
        add_card_num.click()
        add_card_num.clear()
        add_card_num.send_keys(card_num)

        add_date = wait.until(
           EC.visibility_of_element_located(
               (
                   AppiumBy.ANDROID_UIAUTOMATOR,
                   'new UiSelector().resourceId("com.halaleats.user:id/expiry_date_edit_text")'
               )
           ))
        add_date.click()
        add_date.clear()
        add_date.send_keys(exp_date)

        add_cvc = wait.until(
           EC.visibility_of_element_located(
               (
                   AppiumBy.ANDROID_UIAUTOMATOR,
                   'new UiSelector().resourceId("com.halaleats.user:id/cvc_edit_text")'
               )
           ))
        add_cvc.click()
        add_cvc.clear()
        add_cvc.send_keys(cvc)

        driver.back()

        # add card holder name
        add_name = wait.until(
           EC.element_to_be_clickable(
               (
                   AppiumBy.ANDROID_UIAUTOMATOR,
                   'new UiSelector().className("android.widget.EditText").instance(2)'
               )
           ))
        add_name.click()
        add_name.clear()
        add_name.send_keys(name)

        driver.back()

        # saves the card
        save_card = wait.until(
           EC.element_to_be_clickable(
               (
                   AppiumBy.ACCESSIBILITY_ID,
                   'Save Card'
               )
           ))
        save_card.click()


    finally:
        driver.quit()