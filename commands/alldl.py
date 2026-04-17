import requests
import os
import time

def register(bot):
    # এপিআই বেস ইউআরএল পাওয়ার ফাংশন
    def get_base_url():
        try:
            res = requests.get("https://raw.githubusercontent.com/mahmudx7/HINATA/main/baseApiUrl.json")
            return res.json().get("mahmud")
        except:
            return "https://api.samir.pw"

    # ১. কমান্ড দিয়ে ডাউনলোড করার ফাংশন
    @bot.message_handler(commands=['alldl', 'dl', 'download'])
    def handle_dl_command(message):
        args = message.text.split()
        if len(args) > 1:
            process_download(message, args[1])
        elif message.reply_to_message and message.reply_to_message.text:
            process_download(message, message.reply_to_message.text)
        else:
            bot.reply_to(message, "⚔️ 𝐁𝐚𝐛𝐲, 𝐩𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐢𝐝𝐞𝐨 𝐥𝐢𝐧𝐤! 🔗")

    # ২. অটোমেটিক লিঙ্ক ডিটেক্টর (Facebook, TikTok, Instagram, YouTube)
    @bot.message_handler(func=lambda m: m.text and any(x in m.text for x in ["facebook.com", "fb.watch", "tiktok.com", "instagram.com", "youtube.com", "youtu.be"]))
    def auto_link_dl(message):
        # মেসেজ থেকে লিঙ্কটি আলাদা করা
        url = message.text.strip()
        process_download(message, url)

    # ৩. মূল ডাউনলোড এবং অটো-ডিলিট ইঞ্জিন
    def process_download(message, url):
        # ক্যাশ ফোল্ডার তৈরি
        if not os.path.exists("cache"):
            os.makedirs("cache")
            
        file_path = f"cache/dl_{int(time.time())}.mp4"
        
        try:
            bot.send_chat_action(message.chat.id, 'upload_video')
            
            # এপিআই থেকে ভিডিও ডাটা সংগ্রহ
            base = get_base_url()
            # এখানে মাহমুদ এবং সামির দুই এপিআই এরই ব্যাকআপ সাপোর্ট রাখা হয়েছে
            api_url = f"{base}/api/download/video?link={url}"
            res = requests.get(api_url).json()
            
            # ভিডিও ইউআরএল খোঁজা
            video_url = res.get('result', {}).get('url') or res.get('url') or res.get('data', {}).get('play')

            if video_url:
                # ভিডিওটি সাময়িকভাবে লোকাল স্টোরেজে সেভ করা
                video_data = requests.get(video_url).content
                with open(file_path, 'wb') as f:
                    f.write(video_data)
                
                # টেলিগ্রামে ভিডিও পাঠানো
                with open(file_path, 'rb') as video_file:
                    bot.send_video(
                        message.chat.id, 
                        video_file, 
                        caption="✅ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞 ⚔️\n🕊️💖 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠"
                    )
            else:
                # যদি প্রথম এপিআই ফেইল করে তবে ব্যাকআপ এপিআই ট্রাই করবে
                backup_url = f"https://api.samir.pw/download/ytdl?url={url}"
                back_res = requests.get(backup_url).json()
                back_video = back_res.get('result', {}).get('url')
                
                if back_video:
                    bot.send_video(message.chat.id, back_video, caption="✅ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝 𝐯𝐢𝐚 𝐁𝐚𝐜𝐤𝐮𝐩 ⚔️")
                else:
                    bot.reply_to(message, "❌ 𝐒𝐨𝐫𝐫𝐲 𝐛𝐚𝐛𝐲, 𝐭𝐡𝐢𝐬 𝐥𝐢𝐧𝐤 𝐢𝐬 𝐧𝐨𝐭 𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐞𝐝!")
                
        except Exception as e:
            print(f"Error: {e}")
            bot.reply_to(message, "⚠️ 𝐒𝐞𝐫𝐯𝐞𝐫 𝐢𝐬 𝐛𝐮𝐬𝐲, 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫!")
        
        finally:
            # ফাইল পাঠানো শেষ হলে অটোমেটিক ডিলিট
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
