import os
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def register(bot: TeleBot, db):
    @bot.message_handler(commands=["support"])
    def support(message):
        support_url = os.getenv("SUPPORT_URL")

        if not support_url:
            bot.reply_to(
                message,
                "❌ Підтримка тимчасово недоступна."
            )
            return

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "❤️ Підтримати Перекурчика",
                url=support_url
            )
        )

        bot.reply_to(
            message,
            "❤️ <b>Підтримати Перекурчика</b>\n\n"
            "Якщо тобі подобається бот і ти хочеш підтримати його розвиток — "
            "можеш закинути будь-яку суму.\n\n"
            "💸 Кошти підуть на хостинг та розвиток проєкту.\n\n"
            "Дякую за підтримку ❤️",
            parse_mode="HTML",
            reply_markup=keyboard
        )