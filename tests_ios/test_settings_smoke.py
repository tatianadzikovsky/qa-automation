# tests_ios/test_settings_smoke.py
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_open_settings_shows_general(driver):
    el = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (AppiumBy.IOS_PREDICATE, 'label == "General" AND type == "XCUIElementTypeCell"')
        )
    )
    assert el.is_displayed()
