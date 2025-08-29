# pages/settings_page.py
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SettingsPage:
    """
    Android Settings main page.
    Provides helpers to wait for Settings and open rows by visible text,
    trying multiple label candidates and auto-scrolling when needed.
    """

    def __init__(self, driver):
        self.driver = driver

    # ---------- basic waits ----------

    def wait_loaded(self, timeout: int = 10):
        """Wait until we are in the Settings app and something is rendered."""
        def _ready(d):
            try:
                # Often the package is com.android.settings; if OEM differs,
                # fall back to "some text view exists" so we don't hang.
                return (
                    d.current_package == "com.android.settings"
                    or len(d.find_elements(AppiumBy.XPATH, "//android.widget.TextView")) > 0
                )
            except Exception:
                return False

        WebDriverWait(self.driver, timeout).until(_ready)
        return self

    # ---------- helpers ----------

    def _click_exact_text(self, text: str, timeout: int = 2) -> bool:
        """Try to click a visible row that matches the exact text."""
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
                )
            )
            el.click()
            return True
        except TimeoutException:
            return False

    def _scroll_text_into_view(self, text: str) -> bool:
        """Use UiScrollable to bring the text into view (no-op if already visible)."""
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("%s")' % text,
            )
            return True
        except Exception:
            return False

    # ---------- public API ----------

    def open_item_by_text(self, *candidates: str) -> bool:
        """
        Click a settings row by trying the provided label candidates in order.
        Example:
            settings.open_item_by_text("Network & internet", "Connections", "Network")
        Returns True on success, False otherwise.
        """
        for label in candidates:
            # Try without scroll first (fast path)
            if self._click_exact_text(label):
                return True

            # Scroll to it and try again
            if self._scroll_text_into_view(label) and self._click_exact_text(label):
                return True

        return False

