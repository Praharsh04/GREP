from playwright.sync_api import sync_playwright
import re

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://gre.myprepclub.com/forum/reading-comprehension-11/"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_timeout(10000)
        
        # Get all links and filter
        links = page.query_selector_all("a.topic-link")
        print(f"Found {len(links)} topic-links")
        
        q_links = []
        for link in links:
            href = link.get_attribute("href")
            text = link.inner_text().strip()
            if href and "/forum/" in href and href.endswith(".html"):
                # Questions usually have a title that doesn't look like a forum section
                if any(x in text for x in ["Rules", "Guide", "Directory", "Vocabulary", "Test", "Score", "Rules"]):
                    continue
                q_links.append((text, href))
        
        print(f"Filtered to {len(q_links)} potential questions")
        for text, href in q_links[:10]:
            print(f"Q: {text} -> {href}")
            
        if q_links:
            # Pick one that looks like a real RC question
            for text, href in q_links:
                 if "passage" in text.lower() or len(text) > 40:
                     q_url = "https://gre.myprepclub.com" + href if href.startswith('/') else href
                     print(f"Navigating to sample RC: {q_url}")
                     page.goto(q_url)
                     page.wait_for_timeout(5000)
                     with open("sample_rc_real.html", "w", encoding="utf-8") as f:
                         f.write(page.content())
                     break

        browser.close()

if __name__ == "__main__":
    run()
