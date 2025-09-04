from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_open_settings_shows_general(driver):
    # Wait for the “General” cell to be present on the root screen
    el = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.IOS_PREDICATE, 'label == "General" AND type == "XCUIElementTypeCell"'))
    )
    assert el.is_displayed()
