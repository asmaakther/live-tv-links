import requests
import json
import os
import time

API_KEY = os.getenv('YOUTUBE_API_KEY')
# আমি চ্যানেলের নামগুলো আরও নিখুঁত করে দিয়েছি যাতে সার্চ রেজাল্ট ভালো আসে
CHANNELS = [
    "Al Jazeera English Live", "Somoy TV Live", "Ekhon TV Live", 
    "Ekattor TV Live", "Jamuna TV Live", "DBC News Live", 
    "Channel i Live", "ATN News Live", "NTV Live", 
    "Rtv Live", "NEWS24 LIVE", "Desh TV Live", 
    "Independent TV Live", "Channel 24 Live"
]

def get_live_url(query):
    # ইউটিউব এপিআই কল
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=live&type=video&q={query}&key={API_KEY}"
    try:
        response = requests.get(url).json()
        if 'items' in response and len(response['items']) > 0:
            video_id = response['items'][0]['id']['videoId']
            # সরাসরি এমবেড লিঙ্ক তৈরি করা
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        return None
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return None

results = []

for channel in CHANNELS:
    print(f"Searching for: {channel}")
    video_url = get_live_url(channel)
    if video_url:
        results.append({"name": channel.replace(" Live", ""), "url": video_url})
    
    # এপিআই রেট লিমিট এড়াতে ১ সেকেন্ড বিরতি
    time.sleep(1)

# ফাইলটি সেভ করা
with open('links.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print("Mission Successful! All links updated.")
