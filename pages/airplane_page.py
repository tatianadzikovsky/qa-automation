# pages/airplane_page.py
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AirplanePage:
    """
    Handles locating and toggling the Airplane mode switch across OEM variants.
    Strategy:
      1) Ensure 'Airplane' row is visible (scroll if needed)
      2) Prefer switch inside the 'Airplane' row
      3) Fallback to common switch ids / class
    """

    AIR_TEXT_CANDIDATES = (
        "Airplane mode",
        "Airplane",
        "Flight mode",
        "Aeroplane mode",      # some locales
    )

    def __init__(self, driver):
        self.driver = driver

    # ---------- helpers ----------

    def _scroll_row_into_view(self) -> bool:
        """Try to scroll any of the candidate airplane labels into view."""
        for txt in self.AIR_TEXT_CANDIDATES:
            try:
                self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("%s")' % txt
                )
                return True
            except Exception:
                continue
        return False

    def _row_element(self, timeout: int = 3):
        """Return the TextView element that labels the airplane setting."""
        for txt in self.AIR_TEXT_CANDIDATES:
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(
                        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{txt}")')
                    )
                )
            except TimeoutException:
                continue
        return None

    def _switch_in_same_row(self, label_el):
        """
        From the label TextView, walk up to the row container and find a Switch/CheckBox inside.
        This handles OEMs where the switch doesn't have a stable id.
        """
        if not label_el:
            return None
        try:
            # Step up to a likely row container (two parents is usually safe for Settings rows)
            row = label_el.find_element(AppiumBy.XPATH, "../../..")
            # Prefer a Switch in the same row
            sw = row.find_elements(AppiumBy.CLASS_NAME, "android.widget.Switch")
            if sw:
                return sw[0]
            # Some OEMs use a CompoundButton/CheckBox
            cb = row.find_elements(AppiumBy.CLASS_NAME, "android.widget.CheckBox")
            if cb:
                return cb[0]
        except Exception:
            pass
        return None

    def _common_switch_fallback(self):
        """
        Fallback to common ids used by AOSP & OEMs, or the first visible Switch on screen.
        """
        candidates = [
            (AppiumBy.ID, "com.android.settings:id/switch_widget"),
            (AppiumBy.ID, "android:id/switch_widget"),
            (AppiumBy.XPATH, "//*[contains(@resource-id,'switch_widget')]"),
            (AppiumBy.CLASS_NAME, "android.widget.Switch"),
        ]
        for by, value in candidates:
            els = self.driver.find_elements(by, value)
            if els:
                return els[0]
        return None

    def _find_switch(self):
        """
        Robust way to get the airplane toggle:
          - make sure row is visible
          - get the row label, then switch in same row
          - fallback to common switch ids
        """
        # 1) try visible without scroll
        label = self._row_element(timeout=2)
        if not label:
            # 2) scroll and retry
            self._scroll_row_into_view()
            label = self._row_element(timeout=3)

        # Prefer a switch within the same row
        sw = self._switch_in_same_row(label)
        if sw:
            return sw

        # Fallbacks
        return self._common_switch_fallback()

    # ---------- public API ----------

    def airplane_is_on(self) -> bool:
        """
        Returns True if the switch is on. OEMs expose state via:
          - checked attribute on Switch/CheckBox
          - 'ON'/'OFF' text (rare); we treat anything with 'checked' truthy as on.
        """
        sw = self._find_switch()
        if not sw:
            raise NoSuchElementException("Could not locate Airplane mode switch")

        # Appium returns 'checked' as 'true'/'false' string on Android widgets
        checked = sw.get_attribute("checked")
        if checked is not None:
            return str(checked).lower() in ("true", "1", "yes")

        # Very rare case: use text content
        txt = (sw.text or "").strip().lower()
        return txt in ("on", "enabled")

    def toggle_airplane(self):
        """Tap the switch to toggle airplane mode. Ensures it is visible first."""
        sw = self._find_switch()
        if not sw:
            # On failure, save a page source to help debugging
            try:
                with open("screenshots/airplane_page_source.xml", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
            except Exception:
                pass
            raise NoSuchElementException("Airplane switch not found to toggle")
        sw.click()


