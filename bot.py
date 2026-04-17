import os
import requests
import re
import csv
from groq import Groq

# 1. استدعاء المخ (Groq) باستخدام المفتاح اللي أمناه في الخزنة
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_lead_with_ai(email):
    """الذكاء الاصطناعي بيحلل الإيميل ويشوف هل صاحبه زبون 'حوت' ولا لأ"""
    try:
        prompt = f"Analyze this potential customer email: {email}. Is this likely a person who buys luxury, high-end, heavyweight streetwear (600 GSM, Old Money style)? Respond with ONLY one word: 'High-Value' or 'Normal'."
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content.strip()
    except:
        return "Normal"

# 2. كلمات البحث الذكية (Targeting)
queries = [
    'site:instagram.com "luxury streetwear collector" "@gmail.com"',
    'site:linkedin.com "fashion entrepreneur" "@gmail.com"',
    'site:facebook.com "quiet luxury fashion" "@gmail.com"',
    'site:twitter.com "hypebeast" "@gmail.com"'
]

def collect_emails():
    all_found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for q in queries:
        url = f"https://www.google.com/search?q={q}&num=30"
        response = requests.get(url, headers=headers)
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
        all_found.extend(emails)
    return list(set(all_found))

# 3. التشغيل وحفظ النتائج مع التقييم
leads = collect_emails()

with open('leads.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # زودنا عمود جديد للتقييم
    writer.writerow(['Email', 'AI_Assessment'])
    
    for email in leads:
        assessment = analyze_lead_with_ai(email)
        writer.writerow([email, assessment])

print(f"Mission Done! {len(leads)} leads analyzed and saved.")
