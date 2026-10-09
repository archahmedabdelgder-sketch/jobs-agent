import requests
from bs4 import BeautifulSoup
import time

print("🔍 وكيل الوظائف الشامل بدأ البحث...\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8'
}

all_jobs = []

# 1. LinkedIn - السعودية
print("--- 1. البحث في LinkedIn السعودية ---")
try:
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=&location=Saudi%20Arabia&start=0"
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, 'lxml')
    cards = soup.find_all('div', class_='base-card')[:7]

    for card in cards:
        title_tag = card.find('h3', class_='base-search-card__title')
        company_tag = card.find('h4', class_='base-search-card__subtitle')
        link_tag = card.find('a', class_='base-card__full-link')

        if title_tag:
            title = title_tag.get_text(strip=True)
            company = company_tag.get_text(strip=True) if company_tag else "غير محدد"
            link = link_tag['href'] if link_tag else ""
            print(f"✅ [LinkedIn] {title} - {company}")
            print(f"🔗 {link}\n")
            all_jobs.append(title)
    if not cards:
        print("⚠️ LinkedIn ما رجع وظائف (حظر مؤقت)\n")
except Exception as e:
    print(f"❌ LinkedIn خطأ: {e}\n")

time.sleep(2)

# 2. RemoteOK - وظائف ريموت (عالمي)
print("--- 2. البحث في RemoteOK (ريموت) ---")
try:
    url = "https://remoteok.com/api"
    r = requests.get(url, headers=headers, timeout=20)
    jobs = r.json()
    count = 0
    for job in jobs[1:]:
        if count >= 5: break
        title = job.get('position', '')
        company = job.get('company', '')
        link = f"https://remoteok.com/remote-jobs/{job.get('slug')}"
        print(f"✅ [RemoteOK] {title} - {company}")
        print(f"🔗 {link}\n")
        count += 1
        all_jobs.append(title)
except Exception as e:
    print(f"❌ RemoteOK خطأ: {e}\n")

time.sleep(2)

# 3. Bayt.com - السعودية (scraping بسيط)
print("--- 3. البحث في Bayt.com السعودية ---")
try:
    url = "https://www.bayt.com/en/saudi-arabia/jobs/"
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, 'lxml')
    cards = soup.select('li.has-pointer-d')[:7]

    for card in cards:
        title_tag = card.select_one('h2 a, h3 a')
        company_tag = card.select_one('.t-mute')
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = "https://www.bayt.com" + title_tag.get('href', '')
            print(f"✅ [Bayt] {title}")
            print(f"🔗 {link}\n")
            all_jobs.append(title)
    if not cards:
        print("⚠️ Bayt: ما لقينا كروت (الموقع غيّر التصميم)\n")
except Exception as e:
    print(f"❌ Bayt خطأ: {e}\
