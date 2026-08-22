from telebot import TeleBot


def register(bot: TeleBot, db, ADMIN_ID):

    @bot.message_handler(commands=['admin'])
    def admin(message):
        if message.from_user.id != ADMIN_ID:
            return

        users = db.get_users_count()
        private_chats = db.get_private_chats_count()
        groups = db.get_group_chats_count()

        bot.reply_to(
            message,
            f"📊 Статистика бота\n\n"
            f"👥 Користувачів: {users}\n"
            f"👤 Особистих чатів: {private_chats}\n"
            f"👥 Груп: {groups}"
        )