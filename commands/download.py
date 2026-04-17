import os
import time
import requests

def register(bot):
    @bot.message_handler(commands=['download', 'dl'])
    def handle_download(message):
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "⚠️ 𝐋𝐢𝐧𝐤 𝐭𝐚 𝐝𝐚𝐨 𝐛𝐚𝐛𝐲! 🔗")

        url = args[1]
        wait_msg = bot.reply_to(message, "⏳ 𝐖𝐚𝐢𝐭 𝐤𝐨𝐫𝐨 𝐛𝐚𝐛𝐞, 𝐯𝐢𝐝𝐞𝐨 𝐭𝐚 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐤𝐨𝐫𝐜𝐡𝐢... ✨")

        if not os.path.exists("cache"): os.makedirs("cache")
        file_path = f"cache/dl_{int(time.time())}.mp4"

        try:
            res = requests.get(url, stream=True, timeout=150)
            if res.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in res.iter_content(chunk_size=8192):
                        if chunk: f.write(chunk)
                
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption=f"✅ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞! ⚔️")
                
                if os.path.exists(file_path): os.remove(file_path) # পাঠানোর পর ডিলিট
                bot.delete_message(message.chat.id, wait_msg.message_id)
            else:
                bot.reply_to(message, "❌ Link kaj korche na shona!")
        except Exception as e:
            bot.reply_to(message, "⚠️ Server busy babe!")
