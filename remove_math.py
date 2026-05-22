import json

def clean_data():
    try:
        with open('tc_sc_rc.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        original_count = len(data['questions'])
        # Keep only Verbal questions and ensure topic isn't math-related
        data['questions'] = [
            q for q in data['questions'] 
            if q.get('section') == 'Verbal' 
            and not any(math_term in q.get('topic', '').lower() for math_term in ['quant', 'math', 'arithmetic', 'geometry', 'statistics', 'number theory', 'algebra', 'counting', 'probability', 'data interpretation'])
        ]
        
        # Re-index IDs
        for i, q in enumerate(data['questions']):
            q['id'] = i + 1
            
        data['meta']['total_questions'] = len(data['questions'])
        
        with open('tc_sc_rc.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Removed {original_count - len(data['questions'])} math/non-verbal questions.")
        print(f"Remaining questions: {len(data['questions'])}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clean_data()
