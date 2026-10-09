import requests

print("🔍 وكيل الوظائف بدأ البحث...")

url = "https://remoteok.com/api"
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    r = requests.get(url, headers=headers, timeout=15)
    jobs = r.json()
    count = 0
    for job in jobs[1:20]:
        if count >= 10:
            break
        title = job.get('position', '')
        company = job.get('company', '')
        link = f"https://remoteok.com/remote-jobs/{job.get('slug')}"
        print(f"✅ {title} - {company}")
        print(f"🔗 {link}\n")
        count += 1
    print("--- تم ---")
except Exception as e:
    print(f"خطأ: {e}")
