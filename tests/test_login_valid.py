from playwright.sync_api import sync_playwright

def test_login_valid():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # go to login page
        page.goto("http://127.0.0.1:5000/login")

        # fill valid login credentials
        page.fill("input[name='email']", "playwright@gmail.com")
        page.fill("input[name='password']", "play123")

        # click login
        page.wait_for_selector("button[type=submit]")
        page.click("button[type=submit]")

        # expect redirect to profile
        page.wait_for_url("http://127.0.0.1:5000/profile", timeout=5000)

        assert "/profile" in page.url

        browser.close()
