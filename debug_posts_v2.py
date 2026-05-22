from bs4 import BeautifulSoup

with open("sample_q_tc_raw.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

found = False
for div in soup.find_all("div"):
    classes = div.get("class", [])
    if classes and any("post" in str(c).lower() for c in classes):
        print(f"Div classes: {classes}")
        print(div.text.strip()[:100])
        print("---")
        found = True
        
if not found:
    print("No post-related divs found.")
