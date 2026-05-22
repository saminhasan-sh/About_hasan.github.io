import os
import sys
import threading
import time
from flask import Flask
from telethon import TelegramClient, events

# ১. Render-কে শান্ত রাখার জন্য একটি সিম্পল ওয়েব সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "বট ২৪ ঘণ্টা সফলভাবে লাইভ আছে! 🚀"

def run_flask():
    # Render অটোমেটিক একটি PORT এনভায়রনমেন্ট ভ্যারিয়েবল দেয়, সেটা না পেলে ৮০৮০ পোর্ট ব্যবহার হবে
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# একটি আলাদা ব্যাকগ্রাউন্ড থ্রেডে ওয়েব সার্ভারটি চালু করা
server_thread = threading.Thread(target=run_flask)
server_thread.daemon = True
server_thread.start()
print("ওয়েব সার্ভার সফলভাবে চালু হয়েছে...")

# ২. টেলিগ্রাম ইউজারবট সেটআপ
# ⚠️ আপনার আসল API ID এবং HASH বসান
api_id = 38886469          
api_hash = '09c8042e8a2dcdae3fd7eacaf796ec07' 

client = TelegramClient('termux_session', api_id, api_hash)

# অটো-রিপ্লাই মেসেজ হ্যান্ডলার
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

print("টেলিグラム ক্লায়েন্ট স্টার্ট হচ্ছে...")

# মূল থ্রেডেই টেলিগ্রাম ক্লায়েন্ট রান করা, যাতে Render এটিকে বন্ধ না করতে পারে
with client:
    print("টেলিগ্রাম ইউজারবট ব্যাকগ্রাউন্ডে সফলভাবে রান হচ্ছে...")
    client.run_until_disconnected()
