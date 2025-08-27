# pages/wifi_page.py
from appium.webdriver.common.appiumby import AppiumBy

class WifiPage:
    def __init__(self, driver):
        self.driver = driver

    _switch_clazz = "android.widget.Switch"
    _possible_titles = ["Wi-Fi", "WLAN", "Wi-Fi preferences", "Wi-Fi & internet"]

    def is_here(self) -> bool:
        # Check screen title text or presence of a Wi-Fi switch
        for text in self._possible_titles:
            els = self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().textContains("{text}")'
            )
            if els:
                return True
        return len(self.driver.find_elements(AppiumBy.CLASS_NAME, self._switch_clazz)) > 0

    def toggle_first_switch(self) -> bool:
        switches = self.driver.find_elements(AppiumBy.CLASS_NAME, self._switch_clazz)
        if not switches:
            return False
        switches[0].click()
        return True

    def get_first_switch_state(self) -> str:
        # On AOSP Settings, the Switch has a "checked" attribute = "true"/"false"
        switches = self.driver.find_elements(AppiumBy.CLASS_NAME, self._switch_clazz)
        if not switches:
            return "unknown"
        return switches[0].get_attribute("checked")  # "true" or "false"

    def screenshot(self, path: str):
        self.driver.save_screenshot(path)
