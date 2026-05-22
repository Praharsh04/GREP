from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # RC forum
        url = "https://gre.myprepclub.com/forum/reading-comprehension-11/"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_timeout(5000)
        
        # Find a real RC question
        links = page.query_selector_all("a.topic-link")
        for link in links:
            href = link.get_attribute("href")
            text = link.inner_text().strip()
            if "passage" in text.lower() or "RC" in text or len(text) > 30:
                full_url = "https://gre.myprepclub.com" + href if href.startswith('/') else href
                print(f"Navigating to RC question: {full_url}")
                page.goto(full_url)
                page.wait_for_timeout(5000)
                with open("sample_rc_raw.html", "w", encoding="utf-8") as f:
                    f.write(page.content())
                break
            
        browser.close()

if __name__ == "__main__":
    run()
