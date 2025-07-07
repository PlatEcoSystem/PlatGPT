import json



with open('result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)



# 1. Загружаем сырой JSON
with open('result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Фильтруем сообщения

cleaned_messages = []
for msg in data['messages']:
    # Пропускаем служебные сообщения
    if msg.get('type') == 'service':
        continue
    

   
    if not isinstance(msg.get('text'), str):
        continue
    
   

    # Пропускаем сообщения без текста
    if not isinstance(msg.get('text'), str):
        continue
    
    # Оставляем только нужные поля

        "from": msg.get("from"),
        "text": msg.get("text")
    
    
    cleaned_messages.append(cleaned_msg)


with open('cleaned_messages.json', 'w', encoding='utf-8') as f:
    json.dump({"messages": cleaned_messages}, f, ensure_ascii=False, indent=2)


# 3. Сохраняем очищенные данные
with open('cleaned_messages.json', 'w', encoding='utf-8') as f:
    json.dump({"messages": cleaned_messages}, f, ensure_ascii=False, indent=2)

print("Очистка завершена! Результат в cleaned_messages.json")

