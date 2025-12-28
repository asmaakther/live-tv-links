import requests
import json
import os
import time

# গিটহাব থেকে দুটি এপিআই কী সংগ্রহ
API_KEYS = [
    os.getenv('YOUTUBE_API_KEY'),
    os.getenv('YOUTUBE_API_KEY_2')
]
FILE_NAME = 'links.json'

CHANNELS = [
    "Al Jazeera English Live", "Somoy TV Live", "Ekhon TV Live", 
    "Ekattor TV Live", "Jamuna TV Live", "DBC News Live", 
    "Channel i Live", "ATN News Live", "NTV Live", 
    "Rtv Live", "NEWS24 LIVE", "Desh TV Live", 
    "Independent TV Live", "Channel 24 Live"
]

def get_live_url(query, keys):
    # এই ফাংশনটি দুটি কী-ই ট্রাই করবে
    for key in keys:
        if not key: continue # কি খালি থাকলে পরেরটাতে যাবে
        
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=live&type=video&q={query}&key={key}"
        try:
            response = requests.get(url).json()
            # যদি এপিআই কোটা শেষ হয়ে যায় (Error 403), তবে পরের কী ট্রাই করবে
            if 'error' in response:
                print(f"কী সমস্যা বা কোটা শেষ, পরের কী ট্রাই করছি...")
                continue 
                
            if 'items' in response and len(response['items']) > 0:
                video_id = response['items'][0]['id']['videoId']
                return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        except:
            continue
    return None

# পুরনো ডাটা লোড (ব্যাকআপ হিসেবে)
old_data = {}
if os.path.exists(FILE_NAME):
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            content = json.load(f)
            old_data = {item['name']: item['url'] for item in content}
    except:
        old_data = {}

new_results = []

for channel in CHANNELS:
    clean_name = channel.replace(" Live", "")
    print(f"Checking: {clean_name}...")
    
    # দুটি কী দিয়ে সার্চ করার চেষ্টা
    new_url = get_live_url(channel, API_KEYS)
    
    if new_url:
        new_results.append({"name": clean_name, "url": new_url})
    elif clean_name in old_data:
        new_results.append({"name": clean_name, "url": old_data[clean_name]})
    
    time.sleep(1)

with open(FILE_NAME, 'w', encoding='utf-8') as f:
    json.dump(new_results, f, indent=4, ensure_ascii=False)

print("সবগুলো লিঙ্ক সফলভাবে আপডেট হয়েছে!")
