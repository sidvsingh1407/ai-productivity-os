from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch()

        # Test Desktop
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto("http://localhost:5173/")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="coming_soon_desktop.png")

        # Test Mobile
        mobile_page = browser.new_page(viewport={"width": 375, "height": 667})
        mobile_page.goto("http://localhost:5173/")
        mobile_page.wait_for_load_state("networkidle")
        mobile_page.screenshot(path="coming_soon_mobile.png")

        browser.close()

if __name__ == "__main__":
    verify()
