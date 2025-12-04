from playwright.sync_api import sync_playwright

def test_login_invalid_password():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Open login page
        page.goto("http://127.0.0.1:5000/login")

        # Enter valid email but wrong password
        page.fill("input[name='email']", "playwright@gmail.com")
        page.fill("input[name='password']", "wrongpass")

        # Click login
        page.wait_for_selector("button[type=submit]")
        page.click("button[type=submit]")

        # Wait for error message to appear
        page.wait_for_selector("text=Invalid login credentials", timeout=5000)

        # Save screenshot of the error state
        page.screenshot(path="invalid_login_error.png", full_page=True)

        # Assert error message is visible
        assert "Invalid login credentials" in page.content()

        browser.close()
