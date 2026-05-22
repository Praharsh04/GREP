from bs4 import BeautifulSoup

with open("sample_q_tc_raw.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Find all divs and see their classes
for div in soup.find_all("div")[:100]:
    classes = div.get("class", [])
    if "post" in classes or any("post" in c for c in classes):
        print(f"Div classes: {classes}")
        print(div.text.strip()[:100])
        print("---")
