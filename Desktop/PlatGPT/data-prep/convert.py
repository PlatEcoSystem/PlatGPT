import json
with open("cleaned_messages.json", "r", encoding="utf-8") as f:
    data = json.load(f)
messages = data["messages"]  
output = []
current = []
for msg in messages:
    author = msg.get("from", "").strip()
    text = msg.get("text", "").strip()

    if not text:
        continue 

    if author == "Платон":
        current.append({"role": "assistant", "content": text})
        if len(current) == 2:
            output.append({"messages": current})
            current = []
    else:
        current = [{"role": "user", "content": text}]

with open("platon_data.jsonl", "w", encoding="utf-8") as f:
    for item in output:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
