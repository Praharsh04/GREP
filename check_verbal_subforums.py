from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://gre.myprepclub.com/forum/gre-verbal-section-4/"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_timeout(5000)
        
        links = page.query_selector_all("a")
        for link in links:
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            if href and "/forum/" in href:
                print(f"{text} -> {href}")
            
        browser.close()

if __name__ == "__main__":
    run()
