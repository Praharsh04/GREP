# Project Progress Summary: GRE Verbal Dataset Normalization

## Work Completed
1.  **Scraping Pipeline Implementation:** 
    *   Developed `gre_scraper.py` using Playwright and BeautifulSoup.
    *   Autonomously crawled GRE Prep Club for Text Completion (TC), Sentence Equivalence (SE), and Reading Comprehension (RC).
    *   Achieved a raw dataset of **1,202 verbal questions**.
2.  **Dataset Cleaning:**
    *   Removed all math/quantitative questions.
    *   Cleared all explanation text to optimize file size and scraping speed.
    *   Removed forum "junk" (timers, promotional text, "Add Notes", "Question Stats").
3.  **Data Repair & Splitting:**
    *   Identified corruption where RC questions were merged into single blocks.
    *   Created `repair_json.py` to split merged questions, extract options from text strings, and normalize the JSON schema.
    *   The repaired dataset now contains **1,862 potential entries** in `tc_sc_rc_cleaned.json`.
4.  **Frontend Analysis:**
    *   Verified `index.html` schema requirements: Questions need `id`, `passage`, `question`, `options` (object), and `correct_answer`.

## Pending Tasks
1.  **Integrity Check:** Verify that the 1,862 questions in `tc_sc_rc_cleaned.json` are structurally sound (valid JSON, balanced brackets).
2.  **Option Alignment:** Ensure every question has a valid `options` object. Currently, some entries (especially newer RC splits) may have empty option sets if parsing failed.
3.  **Final Normalization:** 
    *   Rename `tc_sc_rc_cleaned.json` to the production `tc_sc_rc.json`.
    *   Ensure IDs are strictly sequential from 1 to N.
    *   Standardize `topic` names to exactly "Text Completion", "Sentence Equivalence", and "Reading Comprehension".
4.  **RC Logic:** Verify that each split RC question is correctly associated with its parent passage.

---

## Continuation Prompt
**Copy and paste the block below to continue the work:**

```text
Finalize the normalization of 'tc_sc_rc_cleaned.json' for production usage in the Verbal Practice section.

TASKS:
1. Verify the structural integrity of 'tc_sc_rc_cleaned.json' (1862 entries).
2. Fix any remaining 'options' parsing issues:
   - If 'options' is empty but question text contains labels (A, B, C...), extract them.
   - Remove any forum junk still lingering in the 'question' or 'passage' fields.
3. Standardize 'topic' fields to: "Text Completion", "Sentence Equivalence", or "Reading Comprehension".
4. Re-index all IDs from 1 to 1862.
5. Perform a final validation check:
   - Ensure every question has at least 3 options (except for specific RC types).
   - Ensure 'correct_answer' is a valid key in the 'options' object (or a comma-separated list for multi-select).
6. Replace the original 'tc_sc_rc.json' with this finalized version.
7. Output a summary of the final question counts by category.
```
