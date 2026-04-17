import requests
import os
import time
import json

# ভিডিও আইডি মনে রাখার জন্য ফাইল (যাতে একই ভিডিও বারবার না আসে)
MEMORY_FILE = "cache/ig_memory.json"

def register(bot):
    # মেমোরি লোড করার ফাংশন
    def load_memory():
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    return set(json.load(f))
            except:
                return set()
        return set()

    # মেমোরি সেভ করার ফাংশন
    def save_memory(memory):
        if not os.path.exists("cache"):
            os.makedirs("cache")
        with open(MEMORY_FILE, "w") as f:
            json.dump(list(memory), f)

    @bot.message_handler(commands=['ig', 'insta', 'anisr2'])
    def handle_ig(message):
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "❐ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚𝐧 𝐚𝐧𝐢𝐦𝐞 𝐧𝐚𝐦𝐞! 🌸")

        query = " ".join(args[1:])
        bot.send_chat_action(message.chat.id, 'upload_video')
        
        if not os.path.exists("cache"):
            os.makedirs("cache")
        
        file_path = f"cache/anisr_{int(time.time())}.mp4"

        try:
            # সার্চ টার্ম একটু উন্নত করা হয়েছে
            search_query = f"{query} edit no watermark"
            
            # টিকউইম এপিআই রিকোয়েস্ট
            api_url = f"https://www.tikwm.com/api/feed/search?keywords={search_query}"
            res = requests.get(api_url, timeout=15).json()
            videos = res.get('data', {}).get('videos', [])

            if not videos:
                return bot.reply_to(message, "❐ 𝐍𝐨 𝐞𝐝𝐢𝐭𝐬 𝐯𝐢𝐝𝐞𝐨 𝐟𝐨𝐮𝐧𝐝 𝐛𝐚𝐛𝐲 🥺")

            # মেমোরি থেকে ডাটা নেওয়া
            insta_memory = load_memory()
            
            selected_video = None
            for v in videos:
                v_id = v.get('video_id')
                if v_id not in insta_memory:
                    selected_video = v
                    insta_memory.add(v_id)
                    break
            
            # যদি সব দেখা হয়ে যায়, মেমোরি ক্লিয়ার করে প্রথম ভিডিওটি নিবে
            if not selected_video:
                insta_memory.clear()
                selected_video = videos[0]
                insta_memory.add(selected_video.get('video_id'))
            
            # মেমোরি সেভ করা (সর্বোচ্চ ১০০টি আইডি রাখবে স্টোরেজ বাঁচাতে)
            if len(insta_memory) > 100:
                insta_memory = set(list(insta_memory)[-50:])
            save_memory(insta_memory)

            video_url = selected_video.get('play')

            if video_url:
                # ভিডিও ডাউনলোড
                video_data = requests.get(video_url, timeout=30).content
                with open(file_path, 'wb') as f:
                    f.write(video_data)

                # টেলিগ্রামে ভিডিও পাঠানো
                with open(file_path, 'rb') as video_file:
                    bot.send_video(
                        message.chat.id, 
                        video_file, 
                        caption="❐ 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐯𝐢𝐝𝐞𝐨 𝐛𝐚𝐛𝐲\n━━━━━━━━━━━━━━\n🕊️💖 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠"
                    )
            else:
                bot.reply_to(message, "❐ ভিডিও লিঙ্ক পাওয়া যায়নি।")

        except Exception as e:
            bot.reply_to(message, "❐ 𝐒𝐞𝐫𝐯𝐞𝐫 𝐢𝐬 𝐛𝐮𝐬𝐲. 𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫!")
        
        finally:
            # অটো-ডিলিট সিস্টেম (Storage Clean)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
