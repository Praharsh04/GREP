import json
try:
    with open('tc_sc_rc.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    questions = data.get('questions', [])
    print(f"Total Questions: {len(questions)}")
    
    counts = {"TC": 0, "SE": 0, "RC": 0}
    for q in questions:
        topic = q.get('topic', '')
        if "Text Completion" in topic: counts["TC"] += 1
        elif "Sentence Equivalence" in topic or "Sentence Completion" in topic: counts["SE"] += 1
        elif "Reading Comprehension" in topic: counts["RC"] += 1
    
    print(f"Breakdown: {counts}")
except Exception as e:
    print(f"Error: {e}")
