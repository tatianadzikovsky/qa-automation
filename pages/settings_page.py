# pages/settings_page.py
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SettingsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_loaded(self):
        # Many ROMs expose either a list or recycler
        try:
            self.wait.until(EC.presence_of_element_located((AppiumBy.ID, "android:id/list")))
        except Exception:
            time.sleep(1.5)
        return self

    def open_item_by_text(self, *labels):
        """
        Scrolls and taps the first matching label.
        Example: page.open_item_by_text("Network & internet", "Internet", "Connections")
        """
        for label in labels:
            try:
                self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
                    f'.scrollTextIntoView("{label}")'
                )
                el = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().text("{label}")'
                )
                el.click()
                return True
            except Exception:
                pass
        # fallback contains()
        try:
            el = self.wait.until(EC.presence_of_element_located((
                AppiumBy.XPATH, '//*[contains(@text,"Network") or contains(@text,"Internet")]'
            )))
            el.click()
            return True
        except Exception:
            return False
