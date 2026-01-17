import telebot
import random
import sqlite3
from flask import Flask
from threading import Thread

# --- إعدادات البوت ---
TOKEN = ' 8423494540:AAFAdd1QwA1W8K3kIHn8A4QLBIaTnrKi-hI  '
bot = telebot.TeleBot(TOKEN)

# --- إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats 
                 (id INTEGER PRIMARY KEY, type TEXT, chat_id INTEGER UNIQUE)''')
    conn.commit()
    conn.close()

def add_data(chat_id, chat_type):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO stats (type, chat_id) VALUES (?, ?)", (chat_type, chat_id))
        conn.commit()
    finally:
        conn.close()

# --- أوامر البوت ---
@bot.message_handler(commands=['start'])
def start(message):
    chat_type = 'user' if message.chat.type == 'private' else 'group'
    add_data(message.chat.id, chat_type)
    bot.reply_to(message, "🎰 بوت الروليت جاهز للعمل!\nاستخدم /play للعب.")

@bot.message_handler(commands=['stats'])
def stats(message):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    users = c.execute("SELECT COUNT(*) FROM stats WHERE type='user'").fetchone()[0]
    groups = c.execute("SELECT COUNT(*) FROM stats WHERE type='group'").fetchone()[0]
    conn.close()
    bot.reply_to(message, f"📊 الإحصائيات:\n👥 مستخدمين: {users}\n🏠 مجموعات: {groups}")

# --- جزء السيرفر لـ Render ---
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل الآن بنجاح!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- التشغيل ---
if __name__ == "__main__":
    init_db()
    keep_alive()
    print("البوت بدأ العمل...")
    bot.infinity_polling()
