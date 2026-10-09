import requests
from bs4 import BeautifulSoup
import time

print("Starting Job Agent...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

all_jobs = []

# 1. LinkedIn Saudi
print("--- 1. LinkedIn Saudi ---")
try:
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=&location=Saudi%20Arabia&start=0"
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, 'lxml')
    cards = soup.find_all('div', class_='base-card')[:7]
    for card in cards:
        t = card.find('h3', class_='base-search-card__title')
        c = card.find('h4', class_='base-search-card__subtitle')
        a = card.find('a', class_='base-card__full-link')
        if t:
            print(f"[LinkedIn] {t.get_text(strip=True)} - {c.get_text(strip=True) if c else ''}")
            print(a['href'] if a else "")
    print("")
except Exception as e:
    print(f"LinkedIn error: {e}\n")

# 2. RemoteOK
print("--- 2. RemoteOK ---")
try:
    r = requests.get("https://remoteok.com/api", headers=headers, timeout=20)
    jobs = r.json()
    for job in jobs[1:6]:
        print(f"[RemoteOK] {job.get('position')} - {job.get('company')}")
        print(f"https://remoteok.com/remote-jobs/{job.get('slug')}\n")
except Exception as e:
    print(f"RemoteOK error: {e}\n")

# 3. Bayt.com
print("--- 3. Bayt Saudi ---")
try:
    r = requests.get("https://www.bayt.com/en/saudi-arabia/jobs/", headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, 'lxml')
    cards = soup.select('li.has-pointer-d')[:7]
    for card in cards:
        title_tag = card.select_one('h2 a, h3 a')
        if title_tag:
            print(f"[Bayt] {title_tag.get_text(strip=True)}")
            print(f"https://www.bayt.com{title_tag.get('href','')}\n")
except Exception as e:
    print(f"Bayt error: {e}\n")

print("--- Done ---")
