import requests
import os
import json
import random
import time

# ভিডিও হিস্ট্রি সেভ করার জন্য পাথ
HISTORY_PATH = "cache/tikHistory.json"

def register(bot):
    # হিস্ট্রি লোড করার ফাংশন
    def get_history():
        if not os.path.exists("cache"):
            os.makedirs("cache")
        if not os.path.exists(HISTORY_PATH):
            return []
        try:
            with open(HISTORY_PATH, "r") as f:
                return json.load(f)
        except:
            return []

    # হিস্ট্রি সেভ করার ফাংশন
    def save_history(history):
        with open(HISTORY_PATH, "w") as f:
            json.dump(history, f)

    @bot.message_handler(commands=['tik', 'tiktok', 'video'])
    def handle_tiktok(message):
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "⚠️ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐲𝐩𝐞 𝐚 𝐯𝐢𝐝𝐞𝐨 𝐨𝐫 𝐬𝐨𝐧𝐠 𝐧𝐚𝐦𝐞!")

        query = " ".join(args[1:])
        bot.send_chat_action(message.chat.id, 'upload_video')
        
        file_path = f"cache/tik_{int(time.time())}.mp4"

        try:
            # টিকটক এপিআই কল
            res = requests.get(f"https://www.tikwm.com/api/feed/search?keywords={query}").json()
            video_list = res.get('data', {}).get('videos', [])

            if not video_list:
                return bot.reply_to(message, "⚠️ 𝐍𝐨 𝐯𝐢𝐝𝐞𝐨 𝐟𝐨𝐮𝐧𝐝!")

            history = get_history()
            
            # আগে পাঠানো হয়নি এমন ভিডিও ফিল্টার করা
            filtered_videos = [v for v in video_list if v.get('video_id') not in history]

            # যদি সব ভিডিও দেখা হয়ে যায়, তবে হিস্ট্রি ক্লিয়ার করে নতুন করে শুরু করা
            if not filtered_videos:
                filtered_videos = video_list
                video_ids = [v.get('video_id') for v in video_list]
                history = [id for id in history if id not in video_ids]

            # প্রথম ১৫টি রেজাল্ট থেকে র‍্যান্ডমলি একটি ভিডিও নেওয়া
            video_data = random.choice(filtered_videos[:15])
            
            # হিস্ট্রিতে ভিডিও আইডি সেভ করা (সর্বোচ্চ ১৫০টি)
            history.append(video_data.get('video_id'))
            if len(history) > 150:
                history.pop(0)
            save_history(history)

            video_url = video_data.get('play')

            if video_url:
                # ভিডিও ডাউনলোড
                response = requests.get(video_url, timeout=20).content
                with open(file_path, 'wb') as f:
                    f.write(response)

                # ভিডিও পাঠানো
                with open(file_path, 'rb') as video_file:
                    bot.send_video(
                        message.chat.id, 
                        video_file, 
                        caption="✅ 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐯𝐢𝐝𝐞𝐨 🕊️💖\n⚔️ 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠"
                    )
            else:
                bot.reply_to(message, "⚠️ ভিডিও লিঙ্ক পাওয়া যায়নি।")

        except Exception as e:
            bot.reply_to(message, "⚠️ 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐮𝐬𝐲! 𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧.")
        
        finally:
            # অটো-ডিলিট সিস্টেম
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
