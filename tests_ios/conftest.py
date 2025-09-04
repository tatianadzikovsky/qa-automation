import os
import pytest
from appium import webdriver

APPIUM_URL = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723")
IOS_DEVICE = os.getenv("IOS_DEVICE", "iPhone 15")
IOS_VERSION = os.getenv("IOS_VERSION", "17.5")

@pytest.fixture(scope="session")
def driver():
    """
    Creates an Appium session against the iOS Simulator Settings app.
    No codesigning needed on a simulator.
    """
    caps = {
        "platformName": "iOS",
        "appium:automationName": "XCUITest",
        "appium:deviceName": IOS_DEVICE,
        "appium:platformVersion": IOS_VERSION,
        # test a system app so we don't need to build our own yet
        "appium:bundleId": "com.apple.Preferences",
        "appium:autoAcceptAlerts": True,
        "appium:newCommandTimeout": 120
    }

    drv = webdriver.Remote(APPIUM_URL, caps)
    yield drv
    drv.quit()
