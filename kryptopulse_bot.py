import telebot
import requests
import os
from keep_alive import keep_alive  # optional if you're using Replit

BOT_TOKEN = "7544415750:AAF2WhDytMQdheNHKGsRRbC3h_bPhveKRNc"
bot = telebot.TeleBot(BOT_TOKEN)

alerts = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to KryptoPulse, your crypto alert assistant!")

@bot.message_handler(commands=["setalert"])
def set_alert(message):
    try:
        _, coin, price = message.text.split()
        alert_price = float(price)
        coin = coin.upper()

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()

        if coin.lower() not in data:
            bot.send_message(message.chat.id, "❌ Invalid coin name. Try BTC, ETH, etc.")
            return

        current_price = data[coin.lower()]["usd"]
        user_id = message.chat.id
        alerts[user_id] = {"coin": coin, "price": alert_price}
        bot.send_message(message.chat.id, f"✅ Alert set for {coin} at ${alert_price}. Current: ${current_price}")

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error: {str(e)}. Format: /setalert BTC 50000")

keep_alive()

print("✅ Bot is live...")
bot.polling(non_stop=True)