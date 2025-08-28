# conftest.py
import os
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture(scope="session")
def driver():
    """
    Starts an Appium session against the local emulator.
    Opens Android Settings (system app) so we don't need an APK.
    """
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.automation_name = "UiAutomator2"
    opts.device_name = "Android Emulator"
    opts.app_package = "com.android.settings"
    opts.app_activity = ".Settings"
    # keeps session alive while pytest starts up
    opts.new_command_timeout = 120

    drv = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=opts)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass

