from playwright.sync_api import sync_playwright, TimeoutError

def test_ing_cookie_accept():
    from playwright.sync_api import TimeoutError

    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            try:
                browser = browser_type.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                # 1 Go to the page
                page.goto("https://www.ing.pl")

                # Poczekaj na CAPTCHA albo przycisk cookie
                captcha_iframe = None

                # captcha_iframe = page.locator('iframe[src*="hcaptcha.com"]')
                # captcha_iframe.wait_for(state="attached", timeout=5000)

                page.wait_for_selector('iframe[src*="hcaptcha.com"]', timeout=5000)

                if captcha_frame is None:
                    captcha_frame = page.frame_locator('iframe[src*="hcaptcha.com"]')
                    checkbox = captcha_frame.locator('#checkbox')
                    checkbox.click()

                # 2 Click "Dostosuj"
                page.wait_for_selector('button.js-cookie-policy-main-settings-button', timeout=5000)
                page.click('button.js-cookie-policy-main-settings-button')

                # 3 Enable "Cookies analityczne"
                page.wait_for_selector('div[name="CpmAnalyticalOption"]', timeout=5000)
                page.click('div[name="CpmAnalyticalOption"]')

                # 4 Accept selected cookies
                page.click('button.js-cookie-policy-settings-decline-button')

                # 5 Check that cookie popup is gone
                assert page.locator('div.cookie-policy').is_hidden(), f"The cookie policy div is not hidden ({browser_type.name})"

                # 6 Check the cookie
                cookies = context.cookies()
                found_cookie = next((cookie for cookie in cookies if cookie['name'] == 'cookiePolicyGDPR'), None)

                assert found_cookie is not None, f"cookiePolicyGDPR cookie not found ({browser_type.name})"
                assert found_cookie['value'] == '3', f"cookiePolicyGDPR cookie value is {found_cookie['value']}, expected 3 ({browser_type.name})"

                print(f"Successfully verified: cookiePolicyGDPR cookie has value {found_cookie['value']} ({browser_type.name})")

            except Exception as e:
                page.screenshot(path=f"ing_error_{browser_type.name}.png")
                print(f"Error: {e}")
                raise e


if __name__ == "__main__":
    test_ing_cookie_accept()