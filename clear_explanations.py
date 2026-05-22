import json

def remove_explanations():
    try:
        with open('tc_sc_rc.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for q in data['questions']:
            q['explanation'] = ""
            
        with open('tc_sc_rc.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print("Removed all existing explanations.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    remove_explanations()
