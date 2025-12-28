import os
import requests

# গিটহাব সিক্রেট থেকে এপিআই কী নেওয়া
API_KEY = os.getenv('YOUTUBE_API_KEY')

# আপনার নতুন চ্যানেলের লিস্ট
CHANNELS = [
    "Al Jazeera Live", "Somoy TV Live", "Ekhon Tv Live", 
    "Ekattor TV Live", "Jamuna Tv Live", "DBC News Live", 
    "Channel i Live", "ATN News Live", "NTV Live", 
    "Rtv Live", "NEWS24 LIVE", "Desh TV Live", 
    "independent TV Live", "Channel 24 Live"
]

def get_live_link(query):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=live&q={query}&key={API_KEY}"
        response = requests.get(url).json()
        
        if 'error' in response:
            return f"Error: {response['error']['message']}"
            
        if 'items' in response and len(response['items']) > 0:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        return "No live stream found"
    except Exception as e:
        return f"Error: {str(e)}"

results = []
for channel in CHANNELS:
    print(f"Searching for {channel}...")
    link = get_live_link(channel)
    results.append(f"{channel}: {link}")

# links.txt ফাইলে সেভ করা
with open("links.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("All links updated successfully!")
