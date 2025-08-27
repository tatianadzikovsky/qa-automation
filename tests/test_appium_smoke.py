import time
from appium import webdriver
from appium.options.android import UiAutomator2Options  # <- Appium options

def test_android_settings_opens():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android Emulator"
    options.app_package = "com.android.settings"
    options.app_activity = ".Settings"

    # Appium 2: you can use http://127.0.0.1:4723 (no /wd/hub needed)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    time.sleep(2)
    assert "<hierarchy" in driver.page_source
    driver.quit()

