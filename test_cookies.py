from playwright.sync_api import sync_playwright

def test_ing_cookie_acceptance():
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            try:
                browser = browser_type.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                # 1 Open the ING website
                page.goto("https://www.ing.pl")

                page.screenshot(path=f"test_web_{browser_type.name}.png")

                # 2 Click button "Dostosuj"
                page.wait_for_selector('button.js-cookie-policy-main-settings-button', timeout=10000)
                page.click('button.js-cookie-policy-main-settings-button')
                
                # 3 Check option "Cookies analityczne"
                page.wait_for_selector('div[name="CpmAnalyticalOption"]', timeout=5000)
                page.click('div[name="CpmAnalyticalOption"]')

                # 4 Click button "Zaakceptuj zaznaczone"
                page.click('button.js-cookie-policy-settings-decline-button')

                assert page.locator('div.cookie-policy').is_hidden(), f"The cookie policy div is not hidden ({browser_type.name})"

                # 5 Verification
                cookies = context.cookies()
                found_cookie = None
                
                for cookie in cookies:
                    if cookie['name'] == 'cookiePolicyGDPR':
                        found_cookie = cookie
                        break
                
                assert found_cookie is not None, f"cookiePolicyGDPR cookie not found ({browser_type.name})"
                assert found_cookie['value'] == '3', f"cookiePolicyGDPR cookie value is {found_cookie['value']}, expected 3 ({browser_type.name})"
                
                print(F"Successfully verified: cookiePolicyGDPR cookie has value {found_cookie['value']} ({browser_type.name})")

            except Exception as e:
                page.screenshot(path="ing_error.png")
                print(f"Error: {e}")
                raise e
            finally:
                context.close()
                browser.close()

test_ing_cookie_acceptance()