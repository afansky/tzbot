import os
import sys
from datetime import datetime

import telegram
from telegram.ext import Updater
import pytz

token = os.environ['TOKEN']
updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def time(update, context):
    logging.info("received time request")

    wroclaw_tz = pytz.timezone('Europe/Warsaw')
    minsk_tz = pytz.timezone('Europe/Minsk')
    pacific_tz = pytz.timezone('US/Pacific')

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="*Minsk*: %s\n"
                                  "*Wroclaw*: %s\n"
                                  "*San Diego*: %s\n" %
                                  (datetime.now(minsk_tz).strftime("%H:%M:%S %d/%B/%Y"),
                                   datetime.now(wroclaw_tz).strftime("%H:%M:%S %d/%B/%Y"),
                                   datetime.now(pacific_tz).strftime("%H:%M:%S %d/%B/%Y")),
                             parse_mode=telegram.ParseMode.MARKDOWN_V2)


from telegram.ext import CommandHandler

start_handler = CommandHandler('time', time)
dispatcher.add_handler(start_handler)

updater.start_webhook(listen="0.0.0.0",
                      port=8443,
                      url_path=token)
updater.bot.set_webhook("https://telegram-time-bot.herokuapp.com/" + token)
updater.idle()

# updater.start_polling()
