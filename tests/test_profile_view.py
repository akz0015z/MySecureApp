from playwright.sync_api import sync_playwright

def test_profile_view_logged_in():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # login first
        page.goto("http://127.0.0.1:5000/login")
        page.fill("input[name='email']", "playwright@gmail.com")
        page.fill("input[name='password']", "play123")
        page.click("button[type=submit]")

        # after login, go to profile
        page.goto("http://127.0.0.1:5000/profile")

        # check that username or bio is visible
        assert "Username:" in page.content()
        assert "Bio:" in page.content()

        
        page.screenshot(path="profile_view_normal.png", full_page=True)

        browser.close()
