import json
import re
import os

INPUT_FILE = "tc_sc_rc.json"
OUTPUT_FILE = "tc_sc_rc_cleaned.json"

JUNK_PATTERNS = [
    r"Show:\s*::\s*OA.*",
    r"Practice QuestionsQuestion:\s*\d+Page:\s*\d+(-\d+)?",
    r"Add Notes",
    r"Question Stats:.*?(based on \d+ sessions)?",
    r"Hide\s*Show\s*timer Statistics",
    r"Part of the project:.*?(Shorter GRE - PREPARATION STRATEGY)?",
    r"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.*",
    r"Free Materials for the GRE.*",
    r"00:00",
    r"Question \d+",
    r"Two Answers",
    r"Official Answer.*?Register/Login\.",
    r"_________________.*",
    r"GRE Prep WhatsApp Community.*",
    r"GRE PREMIUM Quant Question Banks.*",
    r"How to achieve your target GRE score.*",
    r"GRE Hard and Tricky VERBAL Practice.*",
    r"GRE Daily Quant Challenge.*",
    r"Signature Read More",
    r"Also replying to the unanswered questions",
    r"The Definitive GRE Vocabulary Masterclass.*",
    r"GRE Beginner: The Definitive Guide",
    r"Shorter GRE - Preparing for the.*",
    r"Gain 20 Kudos & Get FREE Access.*",
    r"Created with Highcharts.*",
    r"Is your answer correct\?",
    r"◯",
    r"\n[A-F]\n"
]

def clean_text(text):
    if not text:
        return ""
    for pattern in JUNK_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()

def parse_options(text):
    options = {}
    # Pattern 1: A. text B. text ...
    matches = re.findall(r"([A-F])[\.\)\t]\s*(.*?)(?=\s+[A-F][\.\)\t]|$)", text, re.DOTALL)
    if matches:
        for label, choice in matches:
            options[label] = choice.strip()
    
    # Pattern 2: (A) text (B) text ...
    if not options:
        matches = re.findall(r"\(([A-F])\)\s*(.*?)(?=\s+\([A-F]\)|$)", text, re.DOTALL)
        for label, choice in matches:
            options[label] = choice.strip()
            
    return options

def extract_answer(text):
    # Look for patterns like "Answer: A, B", "OA: C", "Answer B", "OA C,E"
    ans_match = re.search(r"(Answer|OA|Correct Answer)[:\s]*([A-F,\s&and]+)", text, re.IGNORECASE)
    if ans_match:
        ans_str = ans_match.group(2).strip().upper()
        # Clean up "A AND B" -> "A,B"
        ans_str = re.sub(r"[\s&AND]+", ",", ans_str)
        ans_str = re.sub(r",+", ",", ans_str)
        return ans_str.strip(",")
    return ""

def repair_dataset():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON is malformed: {e}")
            # If it's malformed, we might need a more aggressive recovery, 
            # but let's assume we can load it for now or try to fix syntax errors first.
            return

    new_questions = []
    
    for q in data.get("questions", []):
        passage = clean_text(q.get("passage", ""))
        question_text = q.get("question", "")
        options = q.get("options", {})
        correct_answer = q.get("correct_answer", "")
        
        # Check if RC with multiple questions
        if "Question 2" in question_text or "Question 2" in passage:
            # This is a merged block. We need to split it.
            # Simplified split for now based on "Question \d" or "2. "
            blocks = re.split(r"Question \d+|(?<=\n)\d\.\s+", question_text)
            # The first block might be part of Q1 or preamble
            for i, block in enumerate(blocks):
                cleaned_block = clean_text(block)
                if len(cleaned_block) < 10: continue
                
                parsed_opts = parse_options(cleaned_block)
                ans = extract_answer(block)
                
                # Try to extract the actual question part (before options)
                q_only = re.split(r"[A-F][\.\)]|\([A-F]\)", cleaned_block)[0].strip()
                
                new_questions.append({
                    "id": len(new_questions) + 1,
                    "source": q.get("source", "GRE Prep Club"),
                    "section": "Verbal",
                    "topic": q.get("topic", "Reading Comprehension"),
                    "difficulty": q.get("difficulty", "N/A"),
                    "passage": passage,
                    "question": q_only,
                    "options": parsed_opts,
                    "correct_answer": ans or correct_answer,
                    "explanation": "",
                    "source_url": q.get("source_url", "")
                })
            continue

        # Normal question processing
        # Extract options from question text if missing or malformed
        combined_text = question_text + " " + str(options)
        parsed_opts = parse_options(combined_text)
        if not parsed_opts and isinstance(options, dict):
            # Try to clean existing options
            parsed_opts = {k: clean_text(v) for k, v in options.items() if len(k) == 1}
            
        # If still no options, try parsing the 'A' key if it contains everything
        if not parsed_opts and "A" in options and len(options["A"]) > 20:
             parsed_opts = parse_options(options["A"])

        # Extract answer if missing
        ans = extract_answer(combined_text) or correct_answer
        
        # Clean question text (remove options part)
        q_only = clean_text(question_text)
        if parsed_opts:
            # Remove option labels and text from the end of the question
            for label, text in parsed_opts.items():
                q_only = q_only.replace(text, "").strip()
            # Remove trailing labels like "A. B. C."
            q_only = re.sub(r"\s*[A-F][\.\)]\s*$", "", q_only).strip()

        new_questions.append({
            "id": len(new_questions) + 1,
            "source": q.get("source", "GRE Prep Club"),
            "section": "Verbal",
            "topic": q.get("topic", "N/A"),
            "difficulty": q.get("difficulty", "N/A"),
            "passage": passage,
            "question": q_only,
            "options": parsed_opts,
            "correct_answer": ans.upper(),
            "explanation": "",
            "source_url": q.get("source_url", "")
        })

    # Final normalization and validation
    final_data = {
        "meta": {
            "total_questions": len(new_questions),
            "sources": data.get("meta", {}).get("sources", [])
        },
        "questions": new_questions
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"Repaired dataset saved to {OUTPUT_FILE}")
    print(f"Total questions: {len(new_questions)}")

if __name__ == "__main__":
    repair_dataset()
