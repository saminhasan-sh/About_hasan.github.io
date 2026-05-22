import os
import asyncio
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# ১. Flask ওয়েব সার্ভার সেটআপ (সার্ভার ২৪ ঘণ্টা জাগিয়ে রাখার জন্য)
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
# আপনার আসল API ID (সংখ্যা) এবং API HASH (লেখা) এখানে বসান
api_id = 38886469          
api_hash = '09c8042e8a2dcdae3fd7eacaf796ec07' 

client = TelegramClient('termux_session', api_id, api_hash)

# --- অটো-রিপ্লাই ফিচার ---
# কেউ আপনাকে পার্সোনাল ইনবক্সে (private) মেসেজ দিলে এই কোডটি কাজ করবে
@client.on(events.NewMessage(incoming=True, private=True))
async def auto_reply_handler(event):
    # আপনি নিজে অন্য আইডি থেকে মেসেজ দিলে বা বট নিজে মেসেজ পাঠালে এটি কাজ করবে না (নিরাপত্তার জন্য)
    if event.is_private:
        sender = await event.get_sender()
        if sender and not sender.is_self:
            # আপনার কাঙ্ক্ষিত মেসেজটি স্বয়ংক্রিয়ভাবে চলে যাবে
            await event.respond("Hello, please stay connected. I’ll get back to you as soon as I’m online again.")

# টেস্ট কমান্ড: আপনি নিজে যেকোনো চ্যাটে .ping লিখলে এটি কাজ করবে
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ping'))
async def ping_handler(event):
    await event.edit('ক্লাউড সার্ভার থেকে ইউজারবট ২৪ ঘণ্টা লাইভ! 🏓🔥')

# মূল ফাংশন
async def main():
    keep_alive()
    print("ওয়েব সার্ভার চালু হয়েছে...")
    await client.start()
    print("টেলিগ্রাম ইউজারবট ব্যাকগ্রাউন্ডে রান হচ্ছে...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
