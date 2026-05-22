import os
import json
import time
import re
import logging
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright, Page, Browser
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://gre.myprepclub.com"
TARGET_FILE = "tc_sc_rc.json"
TARGET_COUNTS = {
    "Text Completion": 400,
    "Sentence Equivalence": 400,
    "Reading Comprehension": 400
}
FORUM_URLS = {
    "Text Completion": f"{BASE_URL}/forum/text-completion-16/",
    "Sentence Equivalence": f"{BASE_URL}/forum/sentence-equivalence-12/",
    "Reading Comprehension": f"{BASE_URL}/forum/reading-comprehension-11/"
}

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

class GREScraper:
    def __init__(self):
        self.data = self._load_existing_data()
        self.seen_urls = {q.get("source_url") for q in self.data["questions"] if q.get("source_url")}
        self.counts = self._get_current_counts()
        
    def _load_existing_data(self) -> Dict[str, Any]:
        if os.path.exists(TARGET_FILE):
            try:
                with open(TARGET_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load {TARGET_FILE}: {e}")
        return {"meta": {"total_questions": 0, "sources": []}, "questions": []}

    def _get_current_counts(self) -> Dict[str, int]:
        counts = {"Text Completion": 0, "Sentence Equivalence": 0, "Reading Comprehension": 0}
        for q in self.data["questions"]:
            topic = q.get("topic", "")
            if "Text Completion" in topic:
                counts["Text Completion"] += 1
            elif "Sentence Equivalence" in topic or "Sentence Completion" in topic:
                counts["Sentence Equivalence"] += 1
            elif "Reading Comprehension" in topic:
                counts["Reading Comprehension"] += 1
        return counts

    def save_data(self):
        self.data["meta"]["total_questions"] = len(self.data["questions"])
        if "sources" not in self.data["meta"]:
            self.data["meta"]["sources"] = []
        if not any(s.get("name") == "GRE Prep Club" for s in self.data["meta"]["sources"]):
            self.data["meta"]["sources"].append({
                "name": "GRE Prep Club",
                "url": BASE_URL,
                "note": "Scraped dataset for TC, SE, and RC"
            })
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        logging.info(f"Progress: TC {self.counts['Text Completion']}, SE {self.counts['Sentence Equivalence']}, RC {self.counts['Reading Comprehension']}")

    def scrape_category(self, category: str, target_count: int):
        logging.info(f"Starting SUPER FAST scrape for {category}. Target: {target_count}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page = context.new_page()
            
            current_url = FORUM_URLS[category]
            while self.counts[category] < target_count and current_url:
                logging.info(f"Listing: {current_url}")
                try:
                    page.goto(current_url, wait_until="domcontentloaded", timeout=20000)
                    page.wait_for_selector(".topic-link", timeout=10000)
                except Exception as e:
                    logging.warning(f"Timeout on {current_url}")
                
                soup = BeautifulSoup(page.content(), "html.parser")
                topic_links = soup.find_all("a", class_="topic-link")
                logging.info(f"Found {len(topic_links)} links on listing.")
                
                q_urls = []
                skipped = 0
                for a in topic_links:
                    href = a.get("href")
                    if not href: continue
                    full_url = BASE_URL + href if href.startswith("/") else href
                    
                    if full_url in self.seen_urls:
                        skipped += 1
                        continue
                        
                    # Basic filtering
                    text = a.text.strip()
                    if any(x in text for x in ["Rules", "Guide", "Directory", "Vocabulary", "Test", "Score", "Intro"]):
                        continue
                    q_urls.append(full_url)
                
                logging.info(f"New URLs: {len(q_urls)}, Skipped (already seen): {skipped}")
                
                for q_url in q_urls:
                    if self.counts[category] >= target_count:
                        break
                    
                    try:
                        question_data = self.scrape_question(page, q_url, category)
                        if question_data:
                            self.data["questions"].append(question_data)
                            self.seen_urls.add(q_url)
                            self.counts[category] += 1
                            if self.counts[category] % 20 == 0: # Save less often to be faster
                                self.save_data()
                    except Exception as e:
                        logging.error(f"Error {q_url}: {e}")
                    
                    # Minimal delay
                    time.sleep(0.1)
                
                # Enhanced Pagination: strictly follow 'arrow-right'
                next_page = soup.find("a", class_="arrow-right")
                if not next_page:
                    next_page = soup.find("a", string=re.compile(r"Next|>", re.I))
                
                if next_page:
                    next_href = next_page.get("href")
                    # Ensure we don't loop back to current or previous
                    new_url = BASE_URL + next_href if next_href.startswith("/") else next_href
                    if new_url != current_url:
                        current_url = new_url
                        logging.info(f"Next page: {current_url}")
                    else:
                        logging.info(f"End of subforum {category} (Same URL)")
                        current_url = None
                else:
                    logging.info(f"End of subforum {category}")
                    current_url = None
            
            browser.close()

    def scrape_question(self, page: Page, url: str, category: str) -> Optional[Dict[str, Any]]:
        try:
            # wait_until commit is faster, but domcontentloaded ensures soup works
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
        except:
            return None
        
        soup = BeautifulSoup(page.content(), "html.parser")
        item_texts = soup.find_all("div", class_="item text")
        if not item_texts:
            return None
        
        question_content = item_texts[0]
        raw_q_text = question_content.text.strip()
        cleaned_q_text = raw_q_text.split("ShowHide Answer")[0].split("_________________")[0].strip()
        
        options = {}
        table = question_content.find("table")
        if table:
            for td in table.find_all("td"):
                text = td.text.strip()
                match = re.match(r"([A-F])[\.\)]\s*(.*)", text)
                if match: options[match.group(1)] = match.group(2).strip()
        
        if not options:
            matches = re.findall(r"([A-F])[\.\)]\s*([^\n]+)", cleaned_q_text)
            for label, choice in matches: options[label] = choice.strip()

        if options:
            for label, choice in options.items():
                cleaned_q_text = cleaned_q_text.replace(f"{label}. {choice}", "").replace(f"{label}) {choice}", "").strip()

        correct_answer = ""
        for it in item_texts[:2]:
            text = it.text.strip()
            if "Answer" in text:
                ans_match = re.search(r"Answer:?\s*([A-F, ]+)", text, re.I)
                if ans_match:
                    correct_answer = ans_match.group(1).strip()
                    break
            green = it.find("span", style=re.compile(r"color:\s*#00a651", re.I))
            if green and "Answer" in green.text:
                ans_match = re.search(r"Answer:?\s*([A-F, ]+)", green.text, re.I)
                if ans_match:
                    correct_answer = ans_match.group(1).strip()
                    break

        passage = ""
        question_text = cleaned_q_text
        if category == "Reading Comprehension":
            if "?" in cleaned_q_text:
                parts = cleaned_q_text.split("?", 1)
                passage, question_text = parts[0].strip() + "?", parts[1].strip()
            else:
                passage = cleaned_q_text

        if len(question_text) < 15:
            return None
            
        return {
            "id": len(self.data["questions"]) + 1,
            "source": "GRE Prep Club",
            "section": "Verbal",
            "topic": category,
            "difficulty": "N/A",
            "passage": passage,
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "explanation": "",
            "source_url": url
        }

def main():
    scraper = GREScraper()
    for category, target in TARGET_COUNTS.items():
        if scraper.counts[category] < target:
            scraper.scrape_category(category, target)
    scraper.save_data()

if __name__ == "__main__":
    main()
