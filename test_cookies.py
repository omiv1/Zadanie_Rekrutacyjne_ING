from playwright.sync_api import sync_playwright

def test_ing_cookie_acceptance():
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = browser_type.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://www.ing.pl")

            page.screenshot(path=f"test_web_{browser_type.name}.png")

            context.close()
            browser.close()

test_ing_cookie_acceptance()