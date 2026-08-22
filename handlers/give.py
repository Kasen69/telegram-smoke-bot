from telebot import TeleBot


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
                "🏅 medal — Медаль за внесок"
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

        if item == "medal":
            item_name = "🏅 Медаль за внесок"
        else:
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

        add_item(user_id, item_name, amount)

        bot.reply_to(
            message,
            f"✅ Предмет видано!\n\n"
            f"👤 ID: {user_id}\n"
            f"🎁 {item_name} ×{amount}"
        )