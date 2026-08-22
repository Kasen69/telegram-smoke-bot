from telebot import TeleBot


def register(bot: TeleBot, db):
    @bot.message_handler(commands=['inventory'])
    def inventory(message):
        user_id = message.from_user.id

        db.add_chat(
            message.chat.id,
            message.chat.type
        )

        items = db.get_inventory(user_id)

        if not items:
            bot.reply_to(
                message,
                "🎒 Інвентар порожній."
            )
            return

        text = "🎒 Твій інвентар\n\n"

        for item in items:
            text += f"• {item['item_name']} ×{item['amount']}\n"

        bot.reply_to(message, text)