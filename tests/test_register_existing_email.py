from playwright.sync_api import sync_playwright

def test_register_existing_email():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # go to register page
        page.goto("http://127.0.0.1:5000/register")

        # fill form with existing email
        page.fill("input[name='username']", "special")
        page.fill("input[name='email']", "special@gmail.com")  # already in DB/app log
        page.fill("input[name='password']", "play123")

        # click Register
        page.wait_for_selector("button[type=submit]")
        page.click("button[type=submit]")

        # expecting flash error
        page.wait_for_selector("text=Email already exists", timeout=5000)

        assert "Email already exists" in page.content()
        page.screenshot(path="existing_email_error.png", full_page=True)

        browser.close()
