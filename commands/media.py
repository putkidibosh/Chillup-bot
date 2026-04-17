import requests
import random

def register(bot):
    @bot.message_handler(commands=['bj', 'car', 'bike', 'meme'])
    def handle_media(message):
        cmd = message.text.split()[0][1:]
        map = {"bj": "bhojpuri dance", "car": "car edit 4k", "bike": "superbike status"}
        
        if cmd == "meme":
            res = requests.get("https://mahmud.free.nf/api/meme").json()
            return bot.send_photo(message.chat.id, res['imageUrl'], caption="🐸 𝐌𝐞𝐦𝐞 ⚔️")
        
        try:
            res = requests.get(f"https://www.tikwm.com/api/feed/search?keywords={map[cmd]}").json()
            v = random.choice(res['data']['videos'])['play']
            bot.send_video(message.chat.id, v, caption=f"⚔️ {cmd.upper()} 𝐕𝐢𝐛𝐞𝐬 🕊️💖")
        except: bot.reply_to(message, "❌ সার্ভার বিজি।")
