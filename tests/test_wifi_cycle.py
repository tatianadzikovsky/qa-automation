# tests/test_wifi_cycle.py
import time
from pages.settings_page import SettingsPage
from pages.network_page import NetworkPage

def test_wifi_cycle(driver):
    # 1) Landing on Settings (driver fixture should start Settings)
    settings = SettingsPage(driver).wait_loaded()

    # 2) Open the Network section (robust to vendor text variations)
    opened = settings.open_network_and_internet()
    assert opened, "Could not open Network & internet / Internet / Connections"

    # 3) On the Network page, find Wi-Fi switch and cycle OFF → ON → OFF
    net = NetworkPage(driver).wait_loaded()
    assert net.is_here(), "Network page didn't load"

    # Ensure OFF
    if net.wifi_is_on():
        net.toggle_wifi()
    assert net.wifi_is_off(), "Wi-Fi should be OFF initially"
    net.screenshot("screenshots/wifi_off.png")

    # Turn ON
    net.toggle_wifi()
    assert net.wifi_is_on(), "Wi-Fi should be ON after toggle"
    net.screenshot("screenshots/wifi_on.png")

    # Turn OFF again
    net.toggle_wifi()
    assert net.wifi_is_off(), "Wi-Fi should be OFF again after second toggle"
    net.screenshot("screenshots/wifi_off_again.png")

    time.sleep(1)  # tiny settle so screenshots differ
