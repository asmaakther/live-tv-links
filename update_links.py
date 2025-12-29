import requests
import json
import os
import time

# গিটহাব সিক্রেটস থেকে এপিআই কী সংগ্রহ
API_KEYS = [
    os.getenv('YOUTUBE_API_KEY'),
    os.getenv('YOUTUBE_API_KEY_2')
]
FILE_NAME = 'links.json'

# চ্যানেল লিস্ট
CHANNELS = [
    "Somoy TV Live", "Ekhon TV Live", "Ekattor TV Live", 
    "Jamuna TV Live", "DBC News Live", "Channel i Live", 
    "ATN News Live", "NTV Bangladesh Live", "Rtv Bangladesh Live", 
    "NEWS24 Bangladesh LIVE", "Desh TV Live", "Independent TV Live", 
    "Channel 24 Live", "Al Jazeera English Live", "Vevo Pop Live",
    "National Geographic Wild Live", "T-Series Music Live"
]

def get_live_url(query, keys):
    for key in keys:
        if not key: continue
        
        # order=date এবং relevanceLanguage=bn যোগ করা হয়েছে আরও নিখুঁত রেজাল্টের জন্য
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=live&type=video&q={query}&order=date&key={key}"
        
        try:
            response = requests.get(url).json()
            
            if 'error' in response:
                print(f"কী সমস্যা বা কোটা শেষ, পরের কী ট্রাই করছি...")
                continue 
                
            if 'items' in response and len(response['items']) > 0:
                video_id = response['items'][0]['id']['videoId']
                # সরাসরি ভিডিও ইউআরএল বা এমবেড ইউআরএল
                return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        except Exception as e:
            print(f"Error fetching data: {e}")
            continue
    return None

# পুরনো ডাটা লোড করা (যাতে এপিআই ফেইল করলে পুরনো লিঙ্ক থাকে)
old_data = {}
if os.path.exists(FILE_NAME):
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            content = json.load(f)
            # নামগুলোকে ছোট হাতের অক্ষরে সেভ করছি যাতে সার্চ করতে সুবিধা হয়
            old_data = {item['name'].lower(): item['url'] for item in content}
    except:
        old_data = {}

new_results = []

for channel in CHANNELS:
    clean_name = channel.replace(" Live", "")
    print(f"Checking: {clean_name}...")
    
    new_url = get_live_url(channel, API_KEYS)
    
    if new_url:
        new_results.append({"name": clean_name, "url": new_url})
    elif clean_name.lower() in old_data:
        # যদি নতুন লিঙ্ক না পাওয়া যায়, তবে পুরনো লিঙ্কটি ব্যবহার করবে
        new_results.append({"name": clean_name, "url": old_data[clean_name.lower()]})
    
    time.sleep(1) # এপিআই রেট লিমিট এড়াতে ১ সেকেন্ড বিরতি

# ফাইল সেভ করা
with open(FILE_NAME, 'w', encoding='utf-8') as f:
    json.dump(new_results, f, indent=4, ensure_ascii=False)

print("সবগুলো লিঙ্ক সফলভাবে আপডেট হয়েছে!")
