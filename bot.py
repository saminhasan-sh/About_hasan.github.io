import os
import threading
from flask import Flask
from telethon import TelegramClient, events

# ১. টেলিগ্রাম ইউজারবট কনফিগারেশন
# ⚠️ আপনার আসল API ID এবং HASH বসাবেন
api_id = 38886469          
api_hash = '09c8042e8a2dcdae3fd7eacaf796ec07' 

client = TelegramClient('termux_session', api_id, api_hash)

# অটো-রিপ্লাই ফিচার
@client.on(events.NewMessage(incoming=True))
async def auto_reply_handler(event):
    if event.is_private:
        sender = await event.get_sender()
        if sender and not sender.is_self:
            await event.respond("Hello, please stay connected. I’ll get back to you as soon as I’m online again.")

# টেস্ট কমান্ড (.ping)
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ping'))
async def ping_handler(event):
    await event.edit('ইউজারবট সফলভাবে লাইভ আছে! 🏓🔥')

def run_telegram():
    print("টেলিগ্রাম ক্লায়েন্ট কানেক্ট করা হচ্ছে...")
    with client:
        print("টেলিগ্রাম ইউজারবট ব্যাকগ্রাউন্ডে সফলভাবে রান করছে...")
        client.run_until_disconnected()

# আলাদা ব্যাকগ্রাউন্ড থ্রেডে টেলিগ্রাম বট চালু করা
bot_thread = threading.Thread(target=run_telegram)
bot_thread.daemon = True
bot_thread.start()


# ২. Render-কে লাইভ রাখার জন্য মেইন থ্রেডে Flask সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "বট ২৪ ঘণ্টা সফলভাবে লাইভ আছে! 🚀"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"ওয়েব সার্ভার চালু হচ্ছে {port} পোর্টে...")
    # মেইন থ্রেডে ফ্ল্যাস্ক রান করলে Render কোনোভাবেই এটিকে বন্ধ করতে পারবে না
    app.run(host='0.0.0.0', port=port)
