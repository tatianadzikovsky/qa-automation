import time
from pages.settings_page import SettingsPage
from pages.network_page import NetworkPage

def test_open_network_and_toggle_first_switch(driver):
    settings = SettingsPage(driver).wait_loaded()
    assert settings.open_item_by_text("Network & internet", "Internet", "Connections", "Network")
    net = NetworkPage(driver)
    assert net.is_here()
    assert net.toggle_first_switch()
    net.screenshot("screenshots/network_after_toggle.png")
    time.sleep(1)





    



