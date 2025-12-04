from playwright.sync_api import sync_playwright

def test_register_normal():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # load register page
        page.goto("http://127.0.0.1:5000/register")

        # fill form
        page.fill("input[name='username']", "playtest")
        page.fill("input[name='email']", "playwright@gmail.com")
        page.fill("input[name='password']", "play123")

        # wait for button + click it
        page.wait_for_selector("button[type=submit]")
        page.click("button[type=submit]")

        # wait for redirect to login
        page.wait_for_url("http://127.0.0.1:5000/login", timeout=5000)

        assert "/login" in page.url

        browser.close()
