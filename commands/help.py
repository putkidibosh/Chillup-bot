def register(bot):
    @bot.message_handler(commands=['help', 'menu', 'cmds'])
    def handle_help(message):
        # এখানে কোনো star symbol ব্যবহার করা হয়নি
        help_text = (
            "⚔️ 𝐌𝐫.𝐊𝐢𝐧𝐠 𝐁𝐨𝐭 𝐌𝐞𝐧𝐮 🕊️💖\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎵 𝐌𝐞𝐝𝐢𝐚 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:\n"
            "❐ /sing - ইউটিউব গান ডাউনলোড\n"
            "❐ /tik - টিকটক ভিডিও ডাউনলোড\n"
            "❐ /download - সরাসরি লিঙ্ক ডাউনলোড\n\n"
            "🎮 𝐆𝐚𝐦𝐞𝐬 & 𝐅𝐮𝐧:\n"
            "❐ /slot - স্লট গেম খেলুন\n"
            "❐ /bal - ব্যালেন্স চেক করুন\n\n"
            "⚙️ 𝐒𝐲𝐬𝐭𝐞𝐦:\n"
            "❐ /start - বট চেক করুন\n"
            "❐ /help - মেনু দেখুন\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🛡️ 𝐀𝐝𝐦𝐢𝐧: @mr_King1430\n"
            "✨ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠"
        )
        
        # কোনো star ছাড়াই রিপ্লাই পাঠানো হচ্ছে
        bot.reply_to(message, help_text)
