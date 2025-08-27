import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # remove this line if you want to see the browser
    d = webdriver.Chrome(options=options)
    d.implicitly_wait(5)
    yield d
    d.quit()

def test_example_domain(driver):
    driver.get("https://example.com")
    assert "Example Domain" in driver.title
    assert driver.find_element(By.TAG_NAME, "h1").text == "Example Domain"
