from bs4 import BeautifulSoup

with open("sample_q_tc_raw.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

for pw in soup.find_all("div", class_="post-wrapper"):
    print("=== Post Wrapper ===")
    # Look for content. It might be in 'item text' or just a div with class 'content'
    content = pw.find("div", class_="content")
    if not content:
        content = pw.find("div", class_="item text")
    
    if content:
        print(content.text.strip()[:200])
    else:
        print("Content not found in this post-wrapper")
    print("---")
