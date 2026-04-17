import requests
import re
import csv

# الكلمات اللي البوت هيدور بيها في جوجل عشان يجمع إيميلات المهتمين
queries = [
    'site:instagram.com "luxury streetwear" "@gmail.com"',
    'site:linkedin.com "streetwear collector" "@gmail.com"',
    'site:facebook.com "high end fashion" "@gmail.com"',
    'site:twitter.com "hypebeast" "@gmail.com"'
]

def search_emails(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = f"https://www.google.com/search?q={query}&num=50"
    try:
        response = requests.get(url, headers=headers)
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
        return emails
    except:
        return []

all_emails = set()
for q in queries:
    print(f"Searching: {q}")
    found = search_emails(q)
    all_emails.update(found)

# حفظ النتائج في ملف اسمه leads.csv
with open('leads.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Email'])
    for email in all_emails:
        writer.writerow([email])

print(f"Done! Found {len(all_emails)} potential leads.")
