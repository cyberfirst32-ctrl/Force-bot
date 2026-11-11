import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os

TOKEN = "9141027270:AAFhWE-cJTlu801O3y9U2EEIw8oJDUTMxIM"
CHANNEL = "@kiranaachannel"

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot Nyala Bre!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

def udah_join(user_id):
    try:
        status = bot.get_chat_member(CHANNEL, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if udah_join(user_id):
        bot.send_message(message.chat.id, "Welcome, udah join! Gas pake botnya.")
    else:
        markup = types.InlineKeyboardMarkup()
        btn_join = types.InlineKeyboardButton("Join Channel Dulu", url=f"https://t.me/{CHANNEL.replace('@','')}")
        btn_cek = types.InlineKeyboardButton("Udah Join, Cek Lagi", callback_data="cek_join")
        markup.add(btn_join)
        markup.add(btn_cek)
        bot.send_message(message.chat.id, "Wajib join channel dulu bre biar bisa pake bot!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "cek_join")
def cek_lagi(call):
    user_id = call.from_user.id
    if udah_join(user_id):
        bot.edit_message_text("Welcome, udah join! Gas pake botnya.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "Lu belum join woy! Join dulu!", show_alert=True)

keep_alive()
print("Bot Jalan...")
bot.polling(none_stop=True)
