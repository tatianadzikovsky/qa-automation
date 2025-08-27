from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class NetworkPage:
    def __init__(self, driver):
        self.driver = driver

    # texts that can appear across Android builds
    _TITLE_TEXTS = ["Network & internet", "Internet", "Connections", "Network"]

    def wait_loaded(self, timeout: int = 8):
        """Wait until activity or any title text indicates we're on the Network screen."""
        def ready(d):
            act = (d.current_activity or "")
            if "Network" in act or "network" in act:
                return True
            for text in self._TITLE_TEXTS:
                if d.find_elements(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().textContains("{text}")'
                ):
                    return True
            return False

        try:
            WebDriverWait(self.driver, timeout).until(ready)
        except TimeoutException:
            pass  # we’ll let is_here() decide

        return self

    def is_here(self) -> bool:
        act = (self.driver.current_activity or "")
        if "Network" in act or "network" in act:
            return True
        for text in self._TITLE_TEXTS:
            if self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().textContains("{text}")'
            ):
                return True
        return False

    def toggle_first_switch(self) -> bool:
        switches = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Switch")
        if switches:
            switches[0].click()
            return True
        return False

    def screenshot(self, path: str):
        self.driver.save_screenshot(path)
