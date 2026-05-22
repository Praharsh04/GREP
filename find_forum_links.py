from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://gre.myprepclub.com/"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_timeout(5000)
        
        with open("home_playwright.html", "w", encoding="utf-8") as f:
            f.write(page.content())
            
        links = page.query_selector_all("a")
        for link in links:
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            if any(x in text for x in ["Text Completion", "Sentence Equivalence", "Reading Comprehension"]):
                print(f"Match: {text} -> {href}")
            
        browser.close()

if __name__ == "__main__":
    run()
