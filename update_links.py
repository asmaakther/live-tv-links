import requests
import json
import os

API_KEY = os.getenv('YOUTUBE_API_KEY')
# এখানে আপনার ২০টি চ্যানেলের নাম দিন
CHANNELS = [
    "Al Jazeera Live", "Somoy TV Live", "Ekhon Tv Live", 
    "Ekattor TV Live", "Jamuna Tv Live", "DBC News Live", 
    "Channel i Live", "ATN News Live", "NTV Live", 
    "Rtv Live", "NEWS24 LIVE", "Desh TV Live", 
    "independent TV Live", "Channel 24 Live"
]
def get_live_id(query):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=live&type=video&q={query}&key={API_KEY}"
    response = requests.get(url).json()
    try:
        return response['items'][0]['id']['videoId']
    except:
        return ""

results = {}
for channel in CHANNELS:
    video_id = get_live_id(channel)
    if video_id:
        results[channel] = video_id

with open('links.json', 'w') as f:
    json.dump(results, f)
