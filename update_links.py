import os
import requests
import json

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNELS = ["Somoy TV Live", "Jamuna Tv Live"]

def get_live_link(query):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=live&q={query}&key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        # এখানে প্রিন্ট হবে কেন কাজ করছে না (গিটহাব অ্যাকশনে দেখা যাবে)
        if 'error' in data:
            print(f"YouTube API Error: {data['error']['message']}")
            return None
            
        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id']['videoId']
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

tv_data = []

# টেস্ট করার জন্য একটি ডামি ডেটা (যদি এপিআই কাজ না করে তাও এটি দেখাবে)
tv_data.append({"name": "Test Channel", "url": "https://www.youtube.com/embed/live_stream?channel=UC_g69p7S_I-k9q69NshS8bw"})

for channel in CHANNELS:
    link = get_live_link(channel)
    if link:
        tv_data.append({"name": channel, "url": link})

with open("links.json", "w", encoding="utf-8") as f:
    json.dump(tv_data, f, indent=4)
