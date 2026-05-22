import os
import asyncio
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# ১. Flask ওয়েব সার্ভার সেটআপ (ক্লাউডে ২৪ ঘণ্টা জাগিয়ে রাখার জন্য)
app = Flask('')

@app.route('/')
def home():
    return "বট ২৪ ঘণ্টা লাইভ আছে! 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# ২. টেলিগ্রাম ইউজারবট সেটআপ
# ⚠️ এখানে অবশ্যই আপনার আসল API ID (সংখ্যা) এবং API HASH (লেখা) বসাবেন
api_id = 38886469          
api_hash = '09c8042e8a2dcdae3fd7eacaf796ec07' 

client = TelegramClient('termux_session', api_id, api_hash)

# --- অফলাইন অটো-রিপ্লাই ফিচার ---
@client.on(events.NewMessage(incoming=True))
async def auto_reply_handler(event):
    # মেসেজটি যদি পার্সোনাল ইনবক্সে (private chat) আসে
    if event.is_private:
        sender = await event.get_sender()
        # মেসেজটি যদি অন্য কেউ দিয়ে থাকে (আপনি নিজে দিলে রিপ্লাই হবে না)
        if sender and not sender.is_self:
            # আপনার কাঙ্ক্ষিত অফলাইন মেসেজটি স্বয়ংক্রিয়ভাবে চলে যাবে
            await event.respond("Hello, please stay connected. I’ll get back to you as soon as I’m online again.")

# টেস্ট কমান্ড (নিজে যেকোনো চ্যাটে .ping লিখে চেক করতে পারবেন)
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ping'))
async def ping_handler(event):
    await event.edit('ইউজারবট সফলভাবে লাইভ আছে! 🏓🔥')

# মূল ফাংশন
async def main():
    keep_alive()
    print("ওয়েব সার্ভার চালু হয়েছে...")
    await client.start()
    print("টেলিগ্রাম ইউজারবট ব্যাকগ্রাউন্ডে রান হচ্ছে...")
    await client.run_until_disconnected()

if name == 'main':
    asyncio.run(main())
