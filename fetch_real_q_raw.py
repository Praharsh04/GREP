from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        q_url = "https://gre.myprepclub.com/forum/while-the-notion-of-sovereignty-today-often-carries-authoritarian-conn-40372.html"
        print(f"Navigating to question: {q_url}")
        page.goto(q_url)
        page.wait_for_timeout(10000)
        
        with open("sample_q_tc_raw.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("Saved sample_q_tc_raw.html")
        
        browser.close()

if __name__ == "__main__":
    run()
