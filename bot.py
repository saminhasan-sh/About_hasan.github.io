import os
import asyncio
from telethon import TelegramClient, events
from flask import Flask
import threading
import time

# ১. Flask ওয়েব সার্ভার সেটআপ
app = Flask('')

@app.route('/')
def home():
    return "বট ২৪ ঘণ্টা লাইভ আছে! 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

# ২. টেলিগ্রাম ইউজারবট সেটআপ
# ⚠️ আপনার আসল API ID এবং HASH বসান
api_id = 38886469          
api_hash = '09c8042e8a2dcdae3fd7eacaf796ec07' 

client = TelegramClient('termux_session', api_id, api_hash)

# --- অফলাইন অটো-রিপ্লাই ফিচার ---
@client.on(events.NewMessage(incoming=True))
async def auto_reply_handler(event):
    if event.is_private:
        sender = await event.get_sender()
        if sender and not sender.is_self:
            await event.respond("Hello, please stay connected. I’ll get back to you as soon as I’m online again.")

# টেস্ট কমান্ড
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ping'))
async def ping_handler(event):
    await event.edit('ইউজারবট সফলভাবে লাইভ আছে! 🏓🔥')

# মূল রানার ফাংশন
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # বোত স্টার্ট করা
    loop.run_until_complete(client.start())
    print("টেলিগ্রাম ইউজারবট ব্যাকগ্রাউন্ডে রান হচ্ছে...")
    
    # সার্ভারকে জাগিয়ে রাখার লুপ
    loop.create_task(client.run_until_disconnected())
    loop.run_forever()

if __name__ == '__main__':
    keep_alive()
    print("ওয়েব সার্ভার চালু হয়েছে...")
    
    # টেলিগ্রাম ক্লায়েন্টকে আলাদা থ্রেডে রান করানো যাতে Render ক্র্যাশ না করে
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # মূল থ্রেডটি চালু রাখা
    while True:
        time.sleep(3600)
