from bs4 import BeautifulSoup

with open("home_playwright.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

for link in soup.find_all("a"):
    href = link.get("href")
    text = link.text.strip()
    if href and "/forum/" in href:
        print(f"{text} -> {href}")
