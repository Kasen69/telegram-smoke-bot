from telebot import TeleBot
from items.items import ITEMS

ADMIN_ID = 879144294


def register(bot: TeleBot, db):
    @bot.message_handler(commands=['give'])
    def give(message):
        if message.from_user.id != ADMIN_ID:
            return

        args = message.text.split()

        if len(args) != 4:
            bot.reply_to(
                message,
                "❌ Використання:\n"
                "/give ID предмет кількість\n\n"
                "Доступні предмети:\n"
                items_list = ""

                for item_id, info in ITEMS.items():
                    items_list += f"{item_id} — {info['name']}\n"
            )
            return

        try:
            user_id = int(args[1])
            item = args[2].lower()
            amount = int(args[3])
        except ValueError:
            bot.reply_to(
                message,
                "❌ ID та кількість повинні бути числами."
            )
            return

        if item not in ITEMS:
            bot.reply_to(
                message,
                "❌ Такого предмета не існує."
            )
            return

        if amount <= 0:
            bot.reply_to(
                message,
                "❌ Кількість повинна бути більшою за 0."
            )
            return

        db.add_item(user_id, item, amount)

        bot.reply_to(
            message,
            "❌ Використання:\n"
            "/give ID предмет кількість\n\n"
            "Доступні предмети:\n"
            f"{items_list}"
        )