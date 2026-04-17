import os
import importlib.util

def register(bot):
    # আপনার টেলিগ্রাম ইউজারনেম অনুযায়ী অ্যাডমিন কন্ট্রোল
    ADMIN_USERNAME = "mr_King1430"

    @bot.message_handler(commands=['cmd'])
    def handle_cmd_installer(message):
        # ইউজারের ইউজারনেম চেক করা
        user_name = message.from_user.username
        
        # অ্যাডমিন চেক
        if user_name != ADMIN_USERNAME:
            return bot.reply_to(message, "❌ এই কমান্ডটি শুধু মাত্র বসের (@mr_King1430) জন্য সংরক্ষিত! ⚔️")

        # কমান্ড ফরম্যাট: /cmd install filename.py [code]
        args = message.text.split(maxsplit=3)
        
        if len(args) < 3 or args[1].lower() != "install":
            return bot.reply_to(message, "⚠️ 𝐅𝐨𝐫𝐦𝐚𝐭: /cmd install [filename].py [code]\n\nঅথবা স্ক্রিপ্টটি রিপ্লাই দিয়ে লিখুন: /cmd install [filename].py")

        file_name = args[2]
        if not file_name.endswith(".py"):
            file_name += ".py"

        # কোড নির্ধারণ করা (মেসেজ বডি অথবা রিপ্লাই থেকে)
        script_code = ""
        if len(args) == 4:
            script_code = args[3]
        elif message.reply_to_message and message.reply_to_message.text:
            script_code = message.reply_to_message.text
        else:
            return bot.reply_to(message, "❌ স্ক্রিপ্টের কোডটি দিন অথবা কোডসহ মেসেজটিতে রিপ্লাই দিন।")

        # বর্তমান ফোল্ডার (commands) এর পাথ নির্ধারণ
        commands_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(commands_dir, file_name)

        try:
            # ফাইলটি নতুন করে তৈরি করা বা রাইট করা
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(script_code)
            
            bot.reply_to(message, f"📥 𝐒𝐜𝐫𝐢𝐩𝐭 '{file_name}' 𝐢𝐧𝐬𝐭𝐚𝐥𝐥𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲! ⚔️")
            
            # সেভ করার পর সরাসরি লোড করার চেষ্টা করা
            try:
                spec = importlib.util.spec_from_file_location(file_name.replace(".py", ""), file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'register'):
                    module.register(bot)
                    bot.send_message(message.chat.id, "⚡ 𝐒𝐜𝐫𝐢𝐩্টটি তাৎক্ষণিকভাবে সচল করা হয়েছে! 🕊️💖")
            except Exception as load_err:
                bot.send_message(message.chat.id, f"⚠️ ফাইল সেভ হয়েছে। ব্যবহারের জন্য বটটি একবার রিস্টার্ট দিন।")

        except Exception as e:
            bot.reply_to(message, f"❌ স্ক্রিপ্ট সেভ করতে সমস্যা হয়েছে: {str(e)}")
