import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download(url, filename):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Downloaded {url} to {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

download("https://greprepclub.com/forum/text-completion-16/", "tc_listing.html")
download("https://greprepclub.com/forum/even-when-the-recession-was-ostensibly-over-26555.html", "tc_question.html")
