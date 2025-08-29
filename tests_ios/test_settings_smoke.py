import time

def test_ios_settings_smoke(driver):
    # Give Settings a moment to be fully foregrounded
    time.sleep(1)
    # Take a screenshot so we always have proof of life in artifacts
    driver.save_screenshot("screenshots/ios_settings_home.png")
    # Simple sanity assertion on session
    status = driver.session.get("capabilities") or {}
    assert status.get("platformName", "").lower() == "ios"
