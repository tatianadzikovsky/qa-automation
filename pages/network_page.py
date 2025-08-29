# pages/network_page.py
import time
from selenium.webdriver.common.by import By
from .base_page import BasePage, DEFAULT_TIMEOUT

class NetworkPage(BasePage):
    TITLE = (By.ID, "com.android.settings:id/action_bar")

    WIFI_SWITCH_IDS = [
        "com.android.settings:id/switch_widget",
        "android:id/switch_widget",
        "com.android.systemui:id/switch_text",
    ]

    WIFI_STATUS_TEXT_IDS = [
        "com.android.settings:id/switch_text",
        "com.android.settings:id/summary_container",
    ]

    def wait_loaded(self):
        # minimal wait to ensure page is present
        try:
            self.wait_visible(self.TITLE, timeout=DEFAULT_TIMEOUT)
        except Exception:
            pass
        return self

    def is_here(self) -> bool:
        try:
            self.wait_visible(self.TITLE, timeout=DEFAULT_TIMEOUT)
            return True
        except Exception:
            return False

    # ---------- helpers ----------
    def _find_wifi_switch(self):
        for rid in self.WIFI_SWITCH_IDS:
            els = self.driver.find_elements(By.ID, rid)
            for el in els:
                if el.is_displayed():
                    return el
        # Fallback: a Switch next to text “Wi-Fi”
        cand = self.driver.find_elements(
            By.XPATH, "//*[@text='Wi-Fi' or @text='Wi-Fi']/following::*[@class='android.widget.Switch'][1]"
        )
        return cand[0] if cand else None

    def _read_wifi_state_text(self) -> str:
        for rid in self.WIFI_STATUS_TEXT_IDS:
            els = self.driver.find_elements(By.ID, rid)
            for el in els:
                if el.is_displayed():
                    txt = (el.text or "").strip().lower()
                    if txt:
                        return txt
        sw = self._find_wifi_switch()
        if sw is not None:
            checked = sw.get_attribute("checked")
            return "on" if str(checked).lower() == "true" else "off"
        return ""

    # ---------- PUBLIC API used by tests ----------
    def wifi_is_on(self) -> bool:
        txt = self._read_wifi_state_text()
        if "on" in txt:
            return True
        if "off" in txt:
            return False
        sw = self._find_wifi_switch()
        if sw is None:
            return False
        return str(sw.get_attribute("checked")).lower() == "true"

    def wifi_is_off(self) -> bool:
        return not self.wifi_is_on()

    def toggle_wifi(self):
        sw = self._find_wifi_switch()
        if sw is None:
            # last resort: tap the row that contains Wi-Fi text
            row = self.driver.find_elements(
                By.XPATH, "//*[contains(@text,'Wi-Fi') or contains(@text,'Wi-Fi')]"
            )
            if row:
                row[0].click()
            else:
                raise AssertionError("Wi-Fi toggle not found")
        else:
            sw.click()
        time.sleep(1)
        return True

