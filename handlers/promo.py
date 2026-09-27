from telebot import TeleBot


def register(bot: TeleBot, db):
    @bot.message_handler(commands=['promo'])
    def promo(message):
        user_id = message.from_user.id

        args = message.text.split(maxsplit=1)

        if len(args) < 2:
            bot.reply_to(
                message,
                "❌ Використання:\n/promo КОД"
            )
            return

        code = args[1].strip().upper()

        promo = db.get_promo(code)

        if promo is None:
            bot.reply_to(
                message,
                "❌ Такого бонус-коду не існує."
            )
            return

        if db.is_promo_used(user_id, code):
            bot.reply_to(
                message,
                "❌ Ти вже використав цей бонус-код."
            )
            return

        if promo["type"] == "reset_cd":
            user = db.get_user(user_id)

            if user is None:
                bot.reply_to(
                    message,
                    "❌ Спочатку скористайся /start."
                )
                return

            db.update_smoke(
                user_id,
                user["smokes"],
                0
            )

            db.use_promo(user_id, code)

            bot.reply_to(
                message,
                "🎉 Бонус-код активовано!\n"
                "⏳ Час очікування скинуто."
            )
            return

        bot.reply_to(
            message,
            "❌ Невідомий тип бонус-коду."
        )