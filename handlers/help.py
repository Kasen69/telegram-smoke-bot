from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


GUIDE_URL = "https://telegra.ph/Pos%D1%96bnik-Perekurchika-10-09"


def register(bot: TeleBot, db):
    @bot.message_handler(commands=["help"])
    def help_command(message):
        db.add_chat(
            message.chat.id,
            message.chat.type
        )

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "📖 Посібник Перекурчика",
                url=GUIDE_URL
            )
        )

        bot.reply_to(
            message,
            "🚬 <b>Посібник Перекурчика</b>",
            parse_mode="HTML",
            reply_markup=keyboard
        )