from playwright.sync_api import sync_playwright

def test_ing_cookie_acceptance():
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = browser_type.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://www.ing.pl")

            page.screenshot(path=f"test_web_{browser_type.name}.png")

            # 1 Klikniecie przycisku "Dostosuj"
            page.wait_for_selector('button.js-cookie-policy-main-settings-button', timeout=10000)
            page.click('button.js-cookie-policy-main-settings-button')
            
            # 2 Zaznaczenie opcji "Cookies analityczne"
            page.wait_for_selector('div[name="CpmAnalyticalOption"]', timeout=5000)
            page.click('div[name="CpmAnalyticalOption"]')

            # 3 Klikniecie przycisku "Zaakceptuj zaznaczone"
            page.click('button.js-cookie-policy-settings-decline-button')

            context.close()
            browser.close()

test_ing_cookie_acceptance()