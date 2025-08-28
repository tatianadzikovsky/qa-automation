# pages/base_page.py
from typing import Iterable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 20

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def tap(self, locator, timeout=DEFAULT_TIMEOUT):
        el = self.wait_clickable(locator, timeout)
        el.click()
        return el

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def screenshot(self, path: str):
        self.driver.save_screenshot(path)

    def tap_by_text(self, *candidates: Iterable[str], timeout=DEFAULT_TIMEOUT):
        """
        Tap the first visible element whose text matches any candidate.
        Works across different Android flavors (“Network & internet”, “Internet”, “Connections”, “Network”).
        """
        # Try standard “text” match
        for text in candidates:
            locator = (By.XPATH, f"//*[@text='{text}']")
            els = self.find_all(locator)
            for el in els:
                if el.is_displayed():
                    el.click()
                    return True

        # Fallback: contains()
        for text in candidates:
            locator = (By.XPATH, f"//*[contains(@text,'{text}')]")
            els = self.find_all(locator)
            for el in els:
                if el.is_displayed():
                    el.click()
                    return True
        return False
