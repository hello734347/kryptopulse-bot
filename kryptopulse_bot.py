import telebot
import requests
from keep_alive import keep_alive  # optional for hosting

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

alerts = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to KryptoPulse Live Bot!\nUse /setalert COIN PRICE to set an alert.\nExample: /setalert BTC 100000")

@bot.message_handler(commands=["setalert"])
def set_alert(message):
    try:
        _, coin, price = message.text.split()
        alert_price = float(price)
        coin = coin.upper()

        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies=usd")
        data = response.json()

        if coin.lower() not in data:
            bot.send_message(message.chat.id, "❌ Invalid coin name. Try BTC, ETH, etc.")
            return

        current_price = data[coin.lower()]["usd"]

        user_id = message.chat.id
        alerts[user_id] = {"coin": coin, "price": alert_price}

        bot.send_message(message.chat.id, f"""✅ Alert Set Successfully!
🎯 Coin: {coin}
💰 Current Price: ${current_price:,.2f}
🔔 Alert Price: ${alert_price:,.2f}
📉 Trigger: When price drops to or below target""")

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Usage: /setalert COIN PRICE\nExample: /setalert BTC 100000")

def check_alerts():
    for user_id, alert in alerts.items():
        coin = alert["coin"]
        target_price = alert["price"]
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies=usd")
        data = response.json()
        current_price = data[coin.lower()]["usd"]

        if current_price <= target_price:
            bot.send_message(user_id, f"""🚨 ALERT!
Coin: {coin}
Price has dropped to: ${current_price:,.2f}""")

keep_alive()  # optional
bot.polling()
