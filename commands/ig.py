import requests
import os
import time
import random

# মেমোরি সেট (যাতে একই ভিডিও বারবার না আসে)
insta_memory = set()

def register(bot):
    @bot.message_handler(commands=['ig', 'insta', 'anisr2'])
    def handle_ig(message):
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚𝐧 𝐚𝐧𝐢𝐦𝐞 𝐧𝐚𝐦𝐞! 🌸")

        query = " ".join(args[1:])
        bot.send_chat_action(message.chat.id, 'upload_video')
        
        # ক্যাশ ফোল্ডার তৈরি
        if not os.path.exists("cache"):
            os.makedirs("cache")
        
        file_path = f"cache/anisr_{int(time.time())}.mp4"

        try:
            search_terms = f"{query} anime edit amv no watermark"
            # টিকটক সার্চ এপিআই ব্যবহার
            res = requests.get(
                f"https://www.tikwm.com/api/feed/search",
                params={"keywords": search_terms},
                timeout=10
            ).json()

            videos = res.get('data', {}).get('videos', [])

            if not videos:
                return bot.reply_to(message, "❌ | 𝐍𝐨 𝐞𝐝𝐢𝐭𝐬 𝐯𝐢𝐝𝐞𝐨 𝐟𝐨𝐮𝐧𝐝 𝐛𝐚𝐛𝐲 <🥹")

            # ভিডিও বাছাই করা (নতুন ভিডিও দেখানোর চেষ্টা করবে)
            selected_video = None
            for v in videos:
                if v.get('video_id') not in insta_memory:
                    selected_video = v
                    break
            
            if not selected_video:
                insta_memory.clear()
                selected_video = videos[0]
            
            insta_memory.add(selected_video.get('video_id'))
            video_url = selected_video.get('play')

            if video_url:
                # ভিডিও ডাউনলোড করে সেভ করা
                video_data = requests.get(video_url, timeout=20).content
                with open(file_path, 'wb') as f:
                    f.write(video_data)

                # টেলিগ্রামে ভিডিও পাঠানো
                with open(file_path, 'rb') as video_file:
                    bot.send_video(
                        message.chat.id, 
                        video_file, 
                        caption="✨ | 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐯𝐢𝐝𝐞𝐨 𝐛𝐚𝐛𝐲\n━━━━━━━━━━━━━━━━━━\n🕊️💖 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠"
                    )
            else:
                bot.reply_to(message, "⚠️ ভিডিও লিঙ্ক পাওয়া যায়নি।")

        except Exception as e:
            bot.reply_to(message, "⚠️ 𝐒𝐞𝐫𝐯𝐞𝐫 𝐢𝐬 𝐛𝐮𝐬𝐲. 𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐢𝐧 𝐚 𝐦𝐨𝐦𝐞𝐧𝐭!")
        
        finally:
            # অটো-ডিলিট সিস্টেম (ফাইল পাঠিয়ে দেওয়ার পর ডিলিট করে দেওয়া)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
