import os
import requests
import json

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNELS = [
    "Al Jazeera Live", "Somoy TV Live", "Ekhon Tv Live",
    "Ekattor TV Live", "Jamuna Tv Live", "DBC News Live",
    "Channel i Live", "ATN News Live", "NTV Live",
    "Rtv Live", "NEWS24 LIVE", "Desh TV Live",
    "independent TV Live", "Channel 24 Live"
]

def get_live_link(query):
    try:
        # ইউটিউবে লাইভ সার্চ করার লিঙ্ক
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=live&q={query}&key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id']['videoId']
            # ব্লগস্পটে চালানোর জন্য এমবেড লিঙ্ক
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        return None
    except Exception as e:
        return None

tv_data = []
for channel in CHANNELS:
    link = get_live_link(channel)
    if link:
        tv_data.append({"name": channel, "url": link})

# ফাইলটি সেভ করা
with open("links.json", "w", encoding="utf-8") as f:
    json.dump(tv_data, f, indent=4)
