from playwright.sync_api import sync_playwright

def test_edit_profile_empty_bio():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # login
        page.goto("http://127.0.0.1:5000/login")
        page.fill("input[name='email']", "playwright@gmail.com")
        page.fill("input[name='password']", "play123")
        page.click("button[type=submit]")

        # go to edit page
        page.goto("http://127.0.0.1:5000/edit_profile")

        # clear bio to trigger error
        page.fill("textarea[name='bio']", "")

        # save
        page.click("button[type=submit]")

        # expect validation error
        page.wait_for_selector("text=Bio cannot be empty", timeout=5000)

        # screenshot for evidence
        page.screenshot(path="edit_profile_empty_bio_error.png")

        assert "Bio cannot be empty" in page.content()

        browser.close()
