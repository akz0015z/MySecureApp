from playwright.sync_api import sync_playwright

def test_edit_profile_normal():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # logs in
        page.goto("http://127.0.0.1:5000/login")
        page.fill("input[name='email']", "playwright@gmail.com")
        page.fill("input[name='password']", "play123")
        page.click("button[type=submit]")

        # goes to edit profile page
        page.goto("http://127.0.0.1:5000/edit_profile")

        # enters valid bio
        new_bio = "This is my new Playwright test for CA3!!"
        page.fill("textarea[name='bio']", new_bio)

        # saves
        page.click("button[type=submit]")

        # redirects to profile
        page.wait_for_url("http://127.0.0.1:5000/profile", timeout=5000)

        # the bio appears
        assert new_bio in page.content()

        # a screenshot showing updated bio
        page.screenshot(path="edit_profile_normal_updated_bio.png")

        browser.close()
