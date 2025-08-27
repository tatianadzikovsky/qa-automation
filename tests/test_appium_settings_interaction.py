import os, time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def make_driver():
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.automation_name = "UiAutomator2"
    opts.device_name = "Android Emulator"
    opts.app_package = "com.android.settings"
    opts.app_activity = ".Settings"
    return webdriver.Remote("http://127.0.0.1:4723", options=opts)

def tap_network_like_item(d):
    # Common labels across Android builds/vendors
    candidates_exact = [
        "Network & internet",
        "Internet",
        "Network",
        "Connections",
    ]
    # 1) Try an exact text hit after a scroll
    for label in candidates_exact:
        try:
            d.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
                f'.scrollTextIntoView("{label}")'
            )
            el = d.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{label}")'
            )
            el.click()
            return True
        except Exception:
            pass

    # 2) Fallback: any item whose text CONTAINS "Network" or "Internet"
    try:
        d.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
            '.scrollForward()'
        )
    except Exception:
        pass  # some screens are already at end

    try:
        el = WebDriverWait(d, 5).until(
            EC.presence_of_element_located((
                AppiumBy.XPATH,
                '//*[contains(@text,"Network") or contains(@text,"Internet")]'
            ))
        )
        el.click()
        return True
    except Exception:
        return False

def test_open_network_and_internet():
    d = make_driver()
    try:
        # Give Settings a moment to render the list
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "android:id/list"))
        )
    except Exception:
        # Some builds don’t expose android:id/list; a small sleep is fine
        time.sleep(2)

    assert tap_network_like_item(d), "Could not find a 'Network/Internet/Connections' item"

    # Quick assertion that we navigated (page shows 'Network' or 'Internet')
    time.sleep(1)
    assert ("Network" in d.page_source) or ("Internet" in d.page_source)

    os.makedirs("screenshots", exist_ok=True)
    d.save_screenshot("screenshots/network_screen.png")
    d.quit()
