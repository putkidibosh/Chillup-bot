import requests
import os
import time
import re

# বেস ইউআরএল পাওয়ার ফাংশন
def get_base_url():
    try:
        res = requests.get("https://raw.githubusercontent.com/mahmudx7/HINATA/main/baseApiUrl.json", timeout=10)
        return res.json().get("mahmud")
    except:
        return "https://mahmud-global-apis.onrender.com"

def register(bot):
    # সাপোর্টেড সাইটগুলোর রেগুলার এক্সপ্রেশন
    supported_sites = re.compile(
        r'https?://(www\.)?(vt\.tiktok\.com|tiktok\.com|facebook\.com|fb\.watch|instagram\.com|youtu\.be|youtube\.com|x\.com|twitter\.com|vm\.tiktok\.com)',
        re.IGNORECASE
    )

    @bot.message_handler(func=lambda message: True if message.text and re.search(r'https?://\S+', message.text) else False)
    def handle_autodl(message):
        text = message.text
        # যদি এটি কোনো কমান্ড হয় (যেমন /start), তবে অটোডাউনলোড কাজ করবে না
        if text.startswith('/'):
            return

        match = re.search(r'https?://\S+', text)
        if not match:
            return
            
        link = match.group(0)
        
        # সাইট ডিটেকশন লজিক
        platform = "𝚄𝚗𝚔𝚗𝚘𝚠𝚗"
        if "facebook.com" in link or "fb.watch" in link:
            platform = "𝐅𝐚𝐜𝐞𝐛𝐨𝐨𝐤"
        elif "instagram.com" in link:
            platform = "𝐈𝐧𝐬𝐭𝐚𝐠𝐫𝐚𝐦"
        elif "tiktok.com" in link:
            platform = "𝐓𝐢𝐤𝐓𝐨𝐤"
        elif "youtu.be" in link or "youtube.com" in link:
            platform = "𝐘𝐨𝐮𝐓𝐮𝐛𝐞"
        elif "x.com" in link or "twitter.com" in link:
            platform = "𝐗 (𝐓𝐰𝐢𝐭𝐭𝐞𝐫)"
        else:
            # যদি চেনা কোনো প্ল্যাটফর্ম না হয় তবে ইগনোর করবে
            return

        if not os.path.exists("cache"):
            os.makedirs("cache")
            
        file_path = f"cache/autodl_{int(time.time())}.mp4"

        try:
            # রিয়্যাকশন পাঠানোর চেষ্টা (টেলিগ্রাম বটে এটি কাজ করার জন্য ইমোজি সেট করতে হয়)
            # অনেক সময় সব বটে রিয়্যাকশন কাজ করে না, তাই এটি সেফলি রাখা হয়েছে
            
            base = get_base_url()
            api_url = f"{base}/api/download/video?link={link}"
            
            # ভিডিও ডাউনলোড শুরু
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }
            
            response = requests.get(api_url, headers=headers, stream=True, timeout=60)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # ফাইল সাইজ চেক (খুব ছোট ফাইল হলে এরর দিবে)
                if os.path.getsize(file_path) < 1000:
                    raise Exception("Invalid video data")

                # ভিডিও পাঠানো
                caption_text = (
                    f"❐ 𝐏𝐥𝐚𝐭𝐟𝐨𝐫𝐦: {platform}\n"
                    "━━━━━━━━━━━━━━\n"
                    "🎬 𝗠𝗿.𝗞𝗶𝗻𝗴 🕊️💖"
                )
                
                with open(file_path, 'rb') as video_file:
                    bot.send_video(
                        message.chat.id, 
                        video_file, 
                        caption=caption_text,
                        reply_to_message_id=message.message_id
                    )
            
        except Exception as e:
            print(f"AutoDL Error: {str(e)}")
            
        finally:
            # ফাইল ডিলিট করে স্টোরেজ ক্লিন রাখা
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
