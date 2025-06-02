
import telebot
import requests
from keep_alive import keep_alive  # optional, for hosting on Render

BOT_TOKEN = "7544415750:AAF2WhDytMQdheNHKGsRRbC3h_bPhveKRNc"
bot = telebot.TeleBot(BOT_TOKEN)

alerts = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to KryptoPulse Live Bot!\nUse /setalert BTC 100000 to set a price alert.")

@bot.message_handler(commands=["setalert"])
def set_alert(message):
    try:
        _, symbol, price = message.text.split()
        alert_price = float(price)

        coin_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "BNB": "binancecoin",
            "DOGE": "dogecoin",
            "SOL": "solana",
            "ADA": "cardano"
        }

        coin = coin_map.get(symbol.upper())

        if not coin:
            bot.send_message(message.chat.id, "❌ Unsupported coin. Try BTC, ETH, BNB, etc.")
            return

        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd")
        data = response.json()

        if coin not in data:
            bot.send_message(message.chat.id, "❌ Invalid coin data from API.")
            return

        current_price = data[coin]["usd"]
        user_id = message.chat.id

        alerts[user_id] = {"coin": coin, "price": alert_price}
        bot.send_message(user_id, f"✅ Alert set for {symbol.upper()} at ${alert_price}. Current price: ${current_price}")

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Error. Use: /setalert BTC 100000")

# Optional keep-alive for hosting
keep_alive()

print("🤖 Bot is polling...")
bot.polling()
