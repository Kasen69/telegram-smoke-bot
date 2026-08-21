from telebot import TeleBot


def register(bot: TeleBot, db):
    @bot.message_handler(commands=["start"])
    def start(message):
        user_id = message.from_user.id
        username = message.from_user.first_name or "Без імені"

        db.add_chat(
            message.chat.id,
            message.chat.type
        )

        user = db.get_user(user_id)

        if user is None:
            db.add_user(user_id, username)

        db.update_username(user_id, username)

        bot.send_message(
            message.chat.id,
            "🚬 Привіт! Я бот-рахівник перекурів.\n\n"
            "Команди:\n"
            "/smoke — покурити\n"
            "/info — твоя статистика\n"
            "/top — топ курців\n"
        )