import os
import requests
import re
import csv
import time
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_lead_with_ai(email):
    try:
        # أمر تحليل سريع عشان ما نستهلكش وقت طويل مع العدد الكبير
        prompt = f"Is {email} likely a luxury fashion buyer? Answer: High or Normal."
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content.strip()
    except:
        return "Normal"

# توسيع قائمة الأهداف لتشمل تيك توك وريديت ومنتديات الموضة
queries = [
    'site:tiktok.com "luxury streetwear" "@gmail.com"',
    'site:reddit.com "r/streetwear" OR "r/repsneakers" "@gmail.com"',
    'site:instagram.com "high-end fashion" "@gmail.com" OR "@icloud.com"',
    'site:facebook.com "luxury car owners" fashion "@gmail.com"',
    'site:fashionforum.com "quiet luxury" "@gmail.com"',
    'site:pinterest.com "aesthetic outfits" "@gmail.com"',
    'site:twitter.com "crypto whale" fashion "@gmail.com"',
    'site:youtube.com "fashion haul" 600gsm "@gmail.com"'
]

def collect_heavy_leads():
    all_found = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for q in queries:
        # بنزود الـ num لـ 100 عشان نسحب داتا أكتر في المرة الواحدة
        url = f"https://www.google.com/search?q={q}&num=100"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
            all_found.extend(emails)
            time.sleep(2) # حماية عشان جوجل ما يعملش بلوك
        except:
            continue
            
    return list(set(all_found))

leads = collect_heavy_leads()

with open('leads.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Email', 'AI_Assessment'])
    
    # هنا البوت هيلف على الـ 500+ إيميل اللي جابهم
    for email in leads:
        assessment = analyze_lead_with_ai(email)
        writer.writerow([email, assessment])

print(f"Target Reached: {len(leads)} leads extracted from all social platforms.")
