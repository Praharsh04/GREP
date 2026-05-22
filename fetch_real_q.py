import re
from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://gre.myprepclub.com/forum/text-completion-16/"
        print(f"Navigating to {url}...")
        page.goto(url)
        
        print("Waiting for content_topic_list...")
        try:
            page.wait_for_selector(".topictitle", timeout=15000)
        except:
            print("Timeout waiting for .topictitle, checking current content...")
            
        with open("tc_listing_ajax.html", "w", encoding="utf-8") as f:
            f.write(page.content())
            
        links = page.query_selector_all("a")
        q_links = []
        for link in links:
            href = link.get_attribute("href")
            text = link.inner_text().strip()
            if href and "/forum/" in href and href.endswith(".html"):
                 # Skip some obvious non-questions
                 if any(x in text for x in ["Rules", "Guide", "Directory", "Vocabulary", "Test", "Score"]):
                     continue
                 if "-" in href:
                     q_links.append((text, href))
                 
        print(f"Found {len(q_links)} potential question links.")
        for text, href in q_links[:10]:
            print(f"Q: {text} -> {href}")
            
        if q_links:
            q_url = "https://gre.myprepclub.com" + q_links[0][1]
            print(f"Navigating to sample question: {q_url}")
            page.goto(q_url)
            page.wait_for_selector(".postbody", timeout=15000)
            with open("sample_q_tc.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            print("Saved sample_q_tc.html")

        browser.close()

if __name__ == "__main__":
    run()
