from telebot import TeleBot
from achievements.achievements import ACHIEVEMENTS


def register(bot: TeleBot, db):
    @bot.message_handler(commands=["achievements"])
    def achievements(message):
        user_id = message.from_user.id

        db.add_chat(
            message.chat.id,
            message.chat.type
        )

        user = db.get_user(user_id)

        if user is None:
            bot.reply_to(
                message,
                "❌ Спочатку скористайся /start."
            )
            return

        unlocked_rows = db.get_achievements(user_id)

        unlocked_ids = {
            row["achievement_id"]
            for row in unlocked_rows
        }

        text = "🏆 <b>Твої досягнення</b>\n\n"

        unlocked_count = 0

        for achievement_id, achievement in ACHIEVEMENTS.items():
            if achievement_id in unlocked_ids:
                unlocked_count += 1

                text += (
                    f"✅ {achievement['name']}\n"
                    f"└ {achievement['description']}\n\n"
                )
            else:
                text += (
                    f"🔒 {achievement['name']}\n"
                    f"└ {achievement['description']}\n\n"
                )

        text += (
            f"🏆 Відкрито: "
            f"<b>{unlocked_count}/{len(ACHIEVEMENTS)}</b>"
        )

        bot.reply_to(
            message,
            text,
            parse_mode="HTML"
        )