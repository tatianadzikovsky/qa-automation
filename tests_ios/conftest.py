import os
import pytest
from appium import webdriver

APPIUM_SERVER = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723/wd/hub")
IOS_DEVICE    = os.getenv("IOS_DEVICE", "iPhone 15")
IOS_VERSION   = os.getenv("IOS_VERSION", "")
IOS_UDID      = os.getenv("IOS_UDID", "")   # provided by the workflow boot step

@pytest.fixture(scope="session")
def driver():
    caps = {
        "platformName": "iOS",
        "appium:automationName": "XCUITest",
        "appium:deviceName": IOS_DEVICE,
        "appium:platformVersion": IOS_VERSION,      # empty is OK
        "appium:bundleId": "com.apple.Preferences", # iOS Settings app
        "appium:autoAcceptAlerts": True,
        "appium:newCommandTimeout": 300,
      }
    if IOS_UDID:
        caps["appium:udid"] = IOS_UDID

    drv = webdriver.Remote(APPIUM_SERVER, caps)
    yield drv
    drv.quit()

