import requests

def register(bot):
    # /tik কমান্ড: টিকটক থেকে ভিডিও খুঁজে দেয়
    @bot.message_handler(commands=['tik', 'video'])
    def handle_tik(message):
        args = message.text.split()
        if len(args) < 2: return bot.reply_to(message, "❌ নাম দিন!")
        query = " ".join(args[1:])
        try:
            res = requests.get(f"https://www.tikwm.com/api/feed/search?keywords={query}").json()
            url = res['data']['videos'][0]['play']
            bot.send_video(message.chat.id, url, caption=f"⚔️ 𝐑𝐞𝐬𝐮𝐥𝐭: {query}")
        except: bot.reply_to(message, "⚠️ ভিডিও পাওয়া যায়নি।")

    # /sing কমান্ড: ইউটিউব থেকে গান (MP3) নামিয়ে দেয়
    @bot.message_handler(commands=['sing', 'song'])
    def handle_sing(message):
        args = message.text.split()
        if len(args) < 2: return bot.reply_to(message, "❌ গানের নাম?")
        query = " ".join(args[1:])
        try:
            s = requests.get(f"https://api.samir.pw/search/youtube?q={query}").json()
            d = requests.get(f"https://api.samir.pw/download/ytdl?url={s[0]['url']}").json()
            bot.send_audio(message.chat.id, d['result']['url'], caption=f"🎵 {query} ⚔️")
        except: bot.reply_to(message, "❌ গানটি পাওয়া যায়নি।")
