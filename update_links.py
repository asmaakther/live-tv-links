import requests
import json
import os
import time

API_KEYS = [
    os.getenv('YOUTUBE_API_KEY'),
    os.getenv('YOUTUBE_API_KEY_2')
]
FILE_NAME = 'links.json'

# এখানে বামপাশে বাটনের নাম (Display Name) এবং ডানপাশে সার্চ কিউয়ার্ড (Search Query)
# বাংলাদেশী চ্যানেলগুলোর জন্য বাংলা ওয়ার্ড যোগ করা হয়েছে
CHANNELS_MAP = {
    "somoy": "Somoy TV Live সময় টিভি লাইভ",
    "ekhon": "Ekhon TV Live এখন টিভি লাইভ",
    "ekattor": "Ekattor TV Live একাত্তর টিভি লাইভ",
    "jamuna": "Jamuna TV Live যমুনা টিভি লাইভ",
    "dbc": "DBC News Live ডিবিসি নিউজ লাইভ",
    "channel i": "Channel i Live চ্যানেল আই লাইভ",
    "atn news": "ATN News Live এটিএন নিউজ লাইভ",
    "ntv": "NTV Bangladesh Live এনটিভি লাইভ",
    "rtv": "Rtv Bangladesh Live আরটিভি লাইভ",
    "news24": "NEWS24 Bangladesh LIVE নিউজ২৪ লাইভ",
    "desh": "Desh TV Live দেশ টিভি লাইভ",
    "independent": "Independent TV Live ইন্ডিপেন্ডেন্ট টিভি লাইভ",
    "channel 24": "Channel 24 Live চ্যানেল ২৪ লাইভ",
    "al jazeera": "Al Jazeera English Live",
    "vevo": "Vevo Pop Live",
    "geographic": "National Geographic Wild Live",
    "t music": "T-Series Music Live"
}

def get_live_url(query, keys):
    for key in keys:
        if not key: continue
        # সার্চে order=date ব্যবহারের বদলে ডিফল্ট প্রাসঙ্গিকতা (relevance) রাখা হয়েছে যাতে অফিসিয়াল চ্যানেল আগে আসে
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=live&type=video&q={query}&key={key}"
        try:
            response = requests.get(url).json()
            if 'error' in response:
                print(f"এপিআই কী সমস্যা, পরবর্তী কী চেষ্টা করা হচ্ছে...")
                continue 
            if 'items' in response and len(response['items']) > 0:
                video_id = response['items'][0]['id']['videoId']
                return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        except:
            continue
    return None

new_results = []

# পুরাতন ডাটা লোড (ব্যাকআপ হিসেবে যদি এপিআই কাজ না করে)
old_data = {}
if os.path.exists(FILE_NAME):
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            content = json.load(f)
            old_data = {item['name']: item['url'] for item in content}
    except:
        pass

for display_name, search_query in CHANNELS_MAP.items():
    print(f"Checking: {display_name}...")
    
    new_url = get_live_url(search_query, API_KEYS)
    
    if new_url:
        new_results.append({"name": display_name, "url": new_url})
    elif display_name in old_data:
        # নতুন লিঙ্ক না পাওয়া গেলে পুরনোটি রেখে দিবে
        new_results.append({"name": display_name, "url": old_data[display_name]})
    
    time.sleep(1)

# ফাইনাল JSON ফাইল সেভ
with open(FILE_NAME, 'w', encoding='utf-8') as f:
    json.dump(new_results, f, indent=4, ensure_ascii=False)

print("সবগুলো চ্যানেল সফলভাবে আপডেট হয়েছে!")
