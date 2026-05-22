from bs4 import BeautifulSoup

with open("tc_listing_real.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

links = soup.find_all("a", class_="topictitle")
for link in links[:10]:
    print(link.get("href"), link.text.strip())

# If topictitle is not found, try something else
if not links:
    print("No topictitle found, trying all forum links...")
    import re
    links = soup.find_all("a", href=re.compile(r"/forum/.*-\d+\.html"))
    for link in links[:10]:
        print(link.get("href"), link.text.strip())
