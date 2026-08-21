from telebot import TeleBot


def register(bot: TeleBot, db):

    @bot.message_handler(commands=['info'])
    def info(message):
        user_id = message.from_user.id

        db.add_chat(
        message.chat.id,
        message.chat.type
        )

        user = db.get_user(user_id)

        if user is None:
            bot.reply_to(message, "У тебе ще немає статистики.")
            return

        username = user["username"]
        count = user["smokes"]

        rank = db.get_user_rank(user_id)

        bot.reply_to(
        message,
        f"📊 Статистика\n\n"
        f"👤 {username}\n"
        f"🚬 Перекурів: {count}\n"
        f"🏆 Місце в топі: #{rank}\n\n"
        f"🔗 https://t.me/perekurbot69"
    )