import requests
import json
import os

API_KEY = os.getenv('YOUTUBE_API_KEY')
# এখানে আপনার ২০টি চ্যানেলের নাম দিন
CHANNELS = ["Somoy TV Live", "Sony TV Live", "Star Sports Live", "Zee Bangla Live"]

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
