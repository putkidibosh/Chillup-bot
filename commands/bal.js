import json
import os

# ব্যালেন্স সেভ করার ফাইল পাথ
BAL_PATH = "cache/user_balances.json"

def register(bot):
    # ডাটা লোড করার ফাংশন
    def load_data():
        if not os.path.exists("cache"):
            os.makedirs("cache")
        if not os.path.exists(BAL_PATH):
            return {}
        try:
            with open(BAL_PATH, "r") as f:
                return json.load(f)
        except:
            return {}

    @bot.message_handler(commands=['bal', 'balance', 'wallet'])
    def handle_balance(message):
        user = message.from_user
        user_id = str(user.id)
        user_name = user.username
        first_name = user.first_name

        # অ্যাডমিন চেক (Mr.King এর জন্য আনলিমিটেড)
        if user_name == "mr_King1430":
            balance_text = "Infinity ♾️"
        else:
            balances = load_data()
            # নতুন ইউজার হলে ৫০০ টাকা ফ্রি বোনাস (উদাহরণস্বরূপ)
            current_bal = balances.get(user_id, 500)
            balance_text = f"💳 {current_bal}"

        # রেসপন্স মেসেজ (কোনো star ব্যবহার করা হয়নি)
        response = (
            "⚔️ 𝐌𝐫.𝐊𝐢𝐧𝐠 𝐖𝐚𝐥𝐥𝐞𝐭 𝐒𝐲𝐬𝐭𝐞𝐦 🕊️💖\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 𝐔𝐬𝐞𝐫: {first_name}\n"
            f"💰 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐁𝐚𝐥𝐚𝐧𝐜𝐞: {balance_text}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✨ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠"
        )

        bot.reply_to(message, response)
