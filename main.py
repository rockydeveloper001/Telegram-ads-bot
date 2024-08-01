from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import requests
from flask import Flask, request
import os

# Replace with your bot token and IPinfo token
TELEGRAM_BOT_TOKEN = '6322113240:AAGVoUcsqY8FZjdRnfLpnsrJOeWBtm5BObI'
IPINFO_TOKEN = 'cdce1e8e5d4e9f'

# Flask app setup
app = Flask(__name__)

# Telegram bot setup
updater = Updater(TELEGRAM_BOT_TOKEN)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Verify", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('👋 Hey There User Welcome To Bot !\n\n🔒 Verify Yourself To Start Bot', reply_markup=reply_markup)

def get_ip_info(ip):
    response = requests.get(f'https://ipinfo.io/{ip}/json?token={IPINFO_TOKEN}')
    return response.json()

def verify(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user_ip = request.remote_addr  # Get user IP address (simplified example)
    ip_info = get_ip_info(user_ip)

    info_message = f"Your IP address is {user_ip}.\n"
    info_message += f"City: {ip_info.get('city', 'N/A')}\n"
    info_message += f"Region: {ip_info.get('region', 'N/A')}\n"
    info_message += f"Country: {ip_info.get('country', 'N/A')}\n"
    info_message += f"ISP: {ip_info.get('org', 'N/A')}"

    query.edit_message_text(text=info_message)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'verify':
        verify(update, context)

# Set up command and callback handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button))

# Flask route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), updater.bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    # Replace 'your-username.pythonanywhere.com' with your actual PythonAnywhere domain
    updater.bot.set_webhook('https://howling-bear-many.on-fleek.app')
    # Start Flask app
    app.run(port=8000)
