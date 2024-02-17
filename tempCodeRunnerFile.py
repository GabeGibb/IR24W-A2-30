import json

file_path = 'full_run/common_words.json'

with open(file_path, 'r') as file:
    data = json.load(file)

top_50_values = sorted(data.values(), key=lambda x: x[1], reverse=True)[:50] #get top 50 values from epiclol
top_50_words = []
for word, value in data.items():
    if value in top_50_values:
        top_50_words.append((word, value))

top_50_words.sort(key=lambda x: x[1], reverse=True) #sort by frequency

for word, frequency in top_50_words:
    print(word, frequency)

