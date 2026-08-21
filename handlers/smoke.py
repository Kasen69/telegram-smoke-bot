from telebot import TeleBot
import time
from config import COOLDOWN


def register(bot: TeleBot, db):
    @bot.message_handler(commands=["smoke"])
    def smoke(message):
        user_id = message.from_user.id
        username = message.from_user.first_name or "Без імені"

        db.add_chat(
            message.chat.id,
            message.chat.type
        )

        current_time = time.time()

        user = db.get_user(user_id)

        if user is None:
            db.add_user(user_id, username)

        db.update_username(user_id, username)
        user = db.get_user(user_id)

        if current_time - user["last_smoke"] >= COOLDOWN:
            new_count = user["smokes"] + 1

            db.update_smoke(
                user_id,
                new_count,
                current_time
            )

            bot.reply_to(
                message,
                f"✅ {username}, ти покурив!\n"
                f"🚬 Всього перекурів: {new_count}"
            )

        else:
            remaining_seconds = int(
                COOLDOWN - (current_time - user["last_smoke"])
            )

            if remaining_seconds >= 300:
                wait_time = f"{remaining_seconds // 60} хв"
            else:
                minutes = remaining_seconds // 60
                seconds = remaining_seconds % 60

                if minutes > 0:
                    wait_time = f"{minutes} хв {seconds} сек"
                else:
                    wait_time = f"{seconds} сек"

            bot.reply_to(
                message,
                f"❌ {username}, ще рано.\n"
                f"⏳ Зачекай приблизно {wait_time}."
            )