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

download("https://gre.myprepclub.com/forum/text-completion-3/", "tc_listing_real.html")
# Let's try to find a question link from the home page if this fails.
