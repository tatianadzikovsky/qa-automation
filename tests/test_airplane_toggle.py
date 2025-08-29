from pages.settings_page import SettingsPage
from pages.airplane_page import AirplanePage
import time

def test_airplane_toggle(driver):
    # App is launched by the driver fixture
    settings = SettingsPage(driver).wait_loaded()

    # Navigate to the section that contains Airplane mode on your device
    assert settings.open_item_by_text("Network & internet", "Connections", "Network")

    air = AirplanePage(driver)
    # Toggle ON
    air.toggle_airplane()
    time.sleep(1)
    assert air.airplane_is_on(), "Airplane mode failed to turn ON"

    # Toggle OFF
    air.toggle_airplane()
    time.sleep(1)
    assert not air.airplane_is_on(), "Airplane mode failed to turn OFF"
