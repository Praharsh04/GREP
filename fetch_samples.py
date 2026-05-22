from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        targets = [
            "https://gre.myprepclub.com/forum/text-completion-16/",
            "https://gre.myprepclub.com/forum/sentence-equivalence-12/",
            "https://gre.myprepclub.com/forum/reading-comprehension-11/"
        ]
        
        for url in targets:
            name = url.split('/')[-2]
            print(f"Fetching listing: {url}")
            page.goto(url)
            page.wait_for_timeout(3000)
            with open(f"listing_{name}.html", "w", encoding="utf-8") as f:
                f.write(page.content())
                
            # Try to get the first question link that looks like a real question
            links = page.query_selector_all("a.topictitle")
            for link in links:
                href = link.get_attribute("href")
                text = link.inner_text().strip()
                # Skip announcements (usually don't have certain patterns or are at top)
                if "Rules" in text or "Guide" in text or "Directory" in text:
                    continue
                
                full_url = "https://gre.myprepclub.com" + href if href.startswith('/') else href
                print(f"Fetching sample question: {full_url}")
                page.goto(full_url)
                page.wait_for_timeout(3000)
                with open(f"question_{name}.html", "w", encoding="utf-8") as f:
                    f.write(page.content())
                break # Just one sample per category
            
        browser.close()

if __name__ == "__main__":
    run()
