from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://gre.myprepclub.com/forum/viewforumtags.php"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_timeout(10000) # Wait 10 seconds for AJAX
        
        with open("tags_playwright.html", "w", encoding="utf-8") as f:
            f.write(page.content())
            
        links = page.query_selector_all("a")
        for link in links:
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            if href and "/forum/" in href and len(text) > 20: # Likely a question title
                print(f"Found question: {text} -> {href}")
            
        browser.close()

if __name__ == "__main__":
    run()
