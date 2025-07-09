import json


with open('result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


cleaned_messages = []
for msg in data['messages']:
    # Пропускаем служебные сообщения
    if msg.get('type') == 'service':
        continue
    
   
    if not isinstance(msg.get('text'), str):
        continue
    
   
    cleaned_msg = {
        "from": msg.get("from"),
        "text": msg.get("text")
    }
    
    cleaned_messages.append(cleaned_msg)


with open('cleaned_messages.json', 'w', encoding='utf-8') as f:
    json.dump({"messages": cleaned_messages}, f, ensure_ascii=False, indent=2)

