
import requests
import time
import telebot
from keep_alive import keep_alive

# Replace with your actual bot token
TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

# Dictionary to hold user alerts
alerts = {}

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to KryptoPulse Live Bot!")


Use /setalert COIN PRICE to set a price alert.
bot.reply_to(message, "Example: /setalert BTC 100000")


# Set alert command
@bot.message_handler(commands=['setalert'])
def set_alert(message):
    try:
        _, coin, price = message.text.split()
        coin = coin.upper()
        price = float(price)
        alerts[message.chat.id] = {"coin": coin, "price": price}
    bot.send_message(message.chat.id, f"""✅ Alert Set Successfully!
🎯 Coin: {coin.upper()}
💰 Current Price: ${current_price:,.2f}
🔔 Alert Price: ${alert_price:,.2f}
📉 Trigger: When price drops to or below target""")
# Function to get current price (using CoinGecko API)
def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data.get(coin.lower(), {}).get("usd")
    
# Background job to check alerts
def check_alerts():
    while True:
        for chat_id, alert in list(alerts.items()):
            price = get_price(alert['coin'])
            if price is not None and price <= alert['price']:
                bot.send_message(chat_id, f"🚨 ALERT!
{alert['coin']} has reached ${price}!")
                del alerts[chat_id]
        time.sleep(60)

# Keep the bot alive
keep_alive()

# Start bot and checker
import threading
threading.Thread(target=check_alerts).start()
bot.polling()
