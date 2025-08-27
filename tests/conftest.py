import os
import pytest
import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture
def driver(request):
    """Fixture to start and quit Appium driver for each test"""
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.automation_name = "UiAutomator2"
    opts.device_name = "Android Emulator"
    opts.app_package = "com.android.settings"
    opts.app_activity = ".Settings"

    drv = webdriver.Remote("http://127.0.0.1:4723", options=opts)

    yield drv

    # Take screenshot if test failed
    if request.node.rep_call.failed:
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{request.node.name}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)

        drv.save_screenshot(filepath)
        print(f"\n📸 Screenshot saved to: {filepath}")

    drv.quit()

# Hook to know if test failed or passed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)





