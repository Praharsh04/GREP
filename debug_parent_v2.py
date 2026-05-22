from bs4 import BeautifulSoup

with open("sample_q_tc_raw.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

for it in soup.find_all("div", class_="item text"):
    if "sovereignty" in it.text.lower():
        print(f"Found it! Parent classes: {it.parent.get('class', 'No class')}")
        print(it.text.strip()[:200])
        print("---")
