import requests
import json
import os
import time

API_KEYS = [
    os.getenv('YOUTUBE_API_KEY'),
    os.getenv('YOUTUBE_API_KEY_2')
]
FILE_NAME = 'links.json'

# এখানে বামপাশে বাটনের নাম (সব ক্যাপিটাল লেটার)
CHANNELS_MAP = {
    "SOMOY TV": "Somoy TV Live সময় টিভি লাইভ",
    "EKHON TV": "Ekhon TV Live এখন টিভি লাইভ",
    "EKATTOR TV": "Ekattor TV Live একাত্তর টিভি লাইভ",
    "JAMUNA TV": "Jamuna TV Live যমুনা টিভি লাইভ",
    "DBC NEWS": "DBC News Live ডিবিসি নিউজ লাইভ",
    "CHANNEL I": "Channel i Live চ্যানেল আই লাইভ",
    "ATN NEWS": "ATN News Live এটিএন নিউজ লাইভ",
    "NTV BANGLA": "NTV Bangladesh Live এনটিভি লাইভ",
    "RTV BANGLA": "Rtv Bangladesh Live আরটিভি লাইভ",
    "NEWS24 BANGLA": "NEWS24 Bangladesh LIVE নিউজ২৪ লাইভ",
    "DESH TV": "Desh TV Live দেশ টিভি লাইভ",
    "INDEPENDENT": "Independent TV Live ইন্ডিপেন্ডেন্ট টিভি লাইভ",
    "CHANNEL 24": "Channel 24 Live চ্যানেল ২৪ লাইভ",
    "AL JAZEERA": "Al Jazeera English Live",
    "ENG MUSIC": "Vevo Pop Live",
    "WILD LIVE": "National Geographic Wild Live",
    "SOUTH MOVIES": "Goldmines Movies Live 24/7 South Indian Hindi Dubbed",
    "HINDI MOVIES": "Bollywood Movies Live Streaming Free",
    "ANIMALLS": "Bangla Movie Live Streaming 24/7",
    "HINDI MUSIC": "T-Series Music Live Hindi Songs 24/7",
    "9XM MUSIC": "9XM Live Bollywood Music"
}
   


def get_live_url(query, keys):
    for key in keys:
        if not key: continue
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=live&type=video&q={query}&key={key}"
        try:
            response = requests.get(url).json()
            if 'items' in response and len(response['items']) > 0:
                video_id = response['items'][0]['id']['videoId']
                return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        except:
            continue
    return None

new_results = []

for display_name, search_query in CHANNELS_MAP.items():
    print(f"Checking: {display_name}...")
    
    new_url = get_live_url(search_query, API_KEYS)
    
    if new_url:
        # এখানে .upper() ব্যবহার করা হয়েছে যাতে নামগুলো ক্যাপিটাল থাকে
        new_results.append({
            "name": display_name.upper(), 
            "url": new_url
        })
    
    time.sleep(1)

with open(FILE_NAME, 'w', encoding='utf-8') as f:
    json.dump(new_results, f, indent=4, ensure_ascii=False)

print("সবগুলো লিঙ্ক ক্যাপিটাল লেটারে আপডেট হয়েছে!")
