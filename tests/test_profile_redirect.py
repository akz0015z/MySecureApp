from playwright.sync_api import sync_playwright

def test_profile_redirect_when_not_logged_in():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Try to access profile WITHOUT logging in
        page.goto("http://127.0.0.1:5000/profile")

        # Expect redirect to login
        page.wait_for_url("http://127.0.0.1:5000/login", timeout=5000)

        # Screenshot for CA3
        page.screenshot(path="profile_redirect.png", full_page=True)

        assert "/login" in page.url

        browser.close()
