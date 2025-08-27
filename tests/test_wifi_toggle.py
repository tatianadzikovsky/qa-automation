# tests/test_wifi_toggle.py
import time
from pages.settings_page import SettingsPage
from pages.wifi_page import WifiPage

def test_wifi_toggle_from_settings(driver):
    # Land on Settings home and navigate into Wi-Fi (paths vary by Android)
    settings = SettingsPage(driver).wait_loaded()

    # Some Android versions have Wi-Fi directly on the home screen.
    # Others put it inside "Network & internet". Try both paths.
    opened = (
        settings.open_item_by_text("Wi-Fi", "WLAN") or
        (settings.open_item_by_text("Network & internet", "Internet", "Connections", "Network")
         and settings.open_item_by_text("Wi-Fi", "WLAN"))
    )
    assert opened, "Couldn't find Wi-Fi entry"

    wifi = WifiPage(driver)
    assert wifi.is_here(), "Not on Wi-Fi page"

    before = wifi.get_first_switch_state()
    assert wifi.toggle_first_switch(), "No Wi-Fi switch found to toggle"
    time.sleep(1)  # brief UI settle
    after = wifi.get_first_switch_state()

    # If we could read the state, assert it actually flipped
    if before in ("true", "false") and after in ("true", "false"):
        assert before != after, f"Wi-Fi switch did not change (before={before}, after={after})"

    wifi.screenshot("screenshots/wifi_after_toggle.png")
