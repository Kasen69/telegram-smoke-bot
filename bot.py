import telebot
import time

from database.database import create_table
from config import TOKEN, ADMIN_ID

from handlers import start
from handlers import smoke
from handlers import info
from handlers import top
from handlers import promo
from handlers import inventory
from handlers import admin
from handlers import give


bot = telebot.TeleBot(TOKEN)

create_table()

import database.database as db
start.register(bot, db)
smoke.register(bot, db)
info.register(bot, db)
top.register(bot, db)
promo.register(bot, db)
inventory.register(bot, db)
give.register(bot, db)
admin.register(bot, db, ADMIN_ID)



#Це має бути останнім!



@bot.message_handler(func=lambda m: True)
def other(message):
    text = message.text.lower()

    if "іді нахуй" in text and "@pitpivo69bot" in text:
        bot.reply_to(message, "сам іді")

    elif text == "іді нахуй":
        bot.reply_to(message, "сам іді")

    elif text == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")


while True:
    try:
        print("Бот запущений...")
        bot.infinity_polling(timeout=30, long_polling_timeout=10)
    except Exception as e:
        print(e)
        print("Перезапуск через 5 секунд...")
        time.sleep(5)
