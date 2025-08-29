# tests_ios/conftest.py
import os, pytest
from appium import webdriver

APPIUM_SERVER = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723/wd/hub")
IOS_DEVICE = os.getenv("IOS_DEVICE", "iPhone 14")      # safe default
IOS_VERSION = os.getenv("IOS_VERSION", "")             # let CI pick latest if empty

@pytest.fixture(scope="session")
def driver():
    caps = {
        "platformName": "iOS",
        "appium:automationName": "XCUITest",
        "appium:deviceName": IOS_DEVICE,
        "appium:platformVersion": IOS_VERSION,      # empty is OK on CI if device exists
        "appium:bundleId": "com.apple.Preferences", # iOS Settings app
        "appium:autoAcceptAlerts": True,
        "appium:newCommandTimeout": 300
    }
    drv = webdriver.Remote(APPIUM_SERVER, caps)
    yield drv
    drv.quit()
