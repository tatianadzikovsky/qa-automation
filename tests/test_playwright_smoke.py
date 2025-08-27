from playwright.sync_api import sync_playwright

def test_example_domain():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # set to False if you want to see the browser
        page = browser.new_page()
        page.goto("https://example.com")
        assert "Example Domain" in page.title()
        assert page.text_content("h1") == "Example Domain"
        browser.close()
