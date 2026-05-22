from bs4 import BeautifulSoup

with open("sample_q_tc_raw.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

item_text = soup.find("div", class_="item text", string=lambda t: t and "sovereignty" in t.lower())
if item_text:
    print(f"Found item text. Parent: {item_text.parent.get('class', 'No class')}")
    # Print more of parent
    print(item_text.parent.text.strip()[:200])
else:
    print("Item text with sovereignty not found")
