import json

file_path = 'full_run/common_words.json'

with open(file_path, 'r') as file:
    data = json.load(file)

top_50_values = sorted(data.values(), reverse=True)[:50] #get top 50 values from epiclolscraper
top_50_words = []
for word, value in data.items():
    if value in top_50_values:
        top_50_words.append((word, value))

top_50_words.sort(key=lambda x: x[1], reverse=True) #sort by frequency

for word, frequency in top_50_words:
    print(word, frequency)


with open('full_run/subdomains.json', 'r') as file:
    data = json.load(file)


for key, value in sorted(data.items()):
    print(f'http://{key}.ics.uci.edu, {value}')
