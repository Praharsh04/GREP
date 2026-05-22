from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Test listing page
        url = "https://gre.myprepclub.com/forum/text-completion-3/"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_timeout(5000) # Wait for content to load
        
        with open("tc_listing_playwright.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        
        # Look for question links
        links = page.query_selector_all("a.topictitle")
        print(f"Found {len(links)} links with class 'topictitle'")
        for link in links[:5]:
            print(f"Text: {link.inner_text().strip()} | Href: {link.get_attribute('href')}")
            
        # Test a single question page
        q_url = "https://gre.myprepclub.com/forum/even-when-the-recession-was-ostensibly-over-26555.html"
        print(f"Navigating to question: {q_url}...")
        page.goto(q_url)
        page.wait_for_timeout(5000)
        
        with open("tc_question_playwright.html", "w", encoding="utf-8") as f:
            f.write(page.content())
            
        browser.close()

if __name__ == "__main__":
    run()
