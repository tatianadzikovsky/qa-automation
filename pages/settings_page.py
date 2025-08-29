# pages/settings_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage, DEFAULT_TIMEOUT

class SettingsPage(BasePage):
    ROOT_LIST = (By.ID, "com.android.settings:id/main_content")  # common container id

    def wait_loaded(self):
        # Wait until the main settings list is visible
        self.wait_visible(self.ROOT_LIST, timeout=DEFAULT_TIMEOUT)
        return self

    def open_network_and_internet(self) -> bool:
        """
        Opens the Network section. We try multiple label variants
        to be robust across Android versions/vendors.
        """
        return self.tap_by_text(
            "Network & internet",
            "Internet",
            "Connections",
            "Network",
        )

