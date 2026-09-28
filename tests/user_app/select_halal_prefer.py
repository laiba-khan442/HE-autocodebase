from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

def test_select_halal_pref():
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

        halal_pref_nav = driver.find_element(
                 AppiumBy.ANDROID_UIAUTOMATOR,
                 'new UiScrollable(new UiSelector().scrollable(true))'
                 '.scrollIntoView(new UiSelector().description("Halal preference"))'
                 )

        halal_pref_nav.click()

        halal_pref_sect = wait.until(
              EC.element_to_be_clickable(
                  (AppiumBy.ACCESSIBILITY_ID,
                      'Select Your Halal Preference'
                  )
              )
          )
        assert halal_pref_sect.is_displayed()

        #selects fully halal-certified badge

        fully_certified = wait.until(
              EC.element_to_be_clickable(
                  (AppiumBy.ANDROID_UIAUTOMATOR,
                      'new UiSelector().className("android.widget.RadioButton").instance(0)'
                  )
              )
          )

        fully_certified.click()


        save_prefer = wait.until(
              EC.element_to_be_clickable(
                  (AppiumBy.ACCESSIBILITY_ID,
                      'Save'
                  )
              )
          )

        save_prefer.click()

# additional assertion to see if account is being displayed.
        assert account_section.is_displayed()

# final toaster assertion
        confirmation = WebDriverWait(
        driver,
        3,
        poll_frequency=0.1
        ).until(
        EC.presence_of_element_located((
        AppiumBy.ACCESSIBILITY_ID,
        "Halal preference saved"
        ))
)


    finally:
        driver.quit()