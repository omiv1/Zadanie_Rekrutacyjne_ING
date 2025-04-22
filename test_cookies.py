from playwright.sync_api import sync_playwright, TimeoutError

def test_ing_cookie_accept():
    from playwright.sync_api import TimeoutError

    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            try:
                browser = browser_type.launch(headless=True)
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080},
                    screen={'width': 1920, 'height': 1080},
                    has_touch=False,
                    is_mobile=False,
                )
                page = context.new_page()
                page.goto("https://www.ing.pl", wait_until="networkidle")

                # Poczekaj na CAPTCHA albo przycisk cookie
                captcha_found = False
                cookie_button_found = False

                try:
                    page.wait_for_selector('iframe[src*="hcaptcha.com"]', timeout=10000)
                    captcha_found = True
                except TimeoutError:
                    pass

                try:
                    page.wait_for_selector('button.js-cookie-policy-main-settings-button', timeout=10000)
                    cookie_button_found = True
                except TimeoutError:
                    pass

                if not captcha_found and not cookie_button_found:
                    raise Exception(f"[{browser_type.name}] Neither CAPTCHA nor cookie settings button appeared")

                if captcha_found:
                    print(f"[{browser_type.name}] CAPTCHA detected")
                    captcha_frame = page.frame_locator('iframe[src*="hcaptcha.com"]')
                    checkbox = captcha_frame.locator('#checkbox')
                    checkbox.click()
                    page.wait_for_selector('iframe[src*="hcaptcha.com"]', state='detached', timeout=15000)
                    print(f"[{browser_type.name}] CAPTCHA passed")
                else:
                    print(f"[{browser_type.name}] No CAPTCHA detected")

                if not cookie_button_found:
                    page.wait_for_selector('button.js-cookie-policy-main-settings-button', timeout=10000)

                # 2 Click "Dostosuj"
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