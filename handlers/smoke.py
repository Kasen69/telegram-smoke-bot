from telebot import TeleBot
import time
import random
from config import COOLDOWN
from achievements.achievements import ACHIEVEMENTS


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

            # Перевірка досягнень
            for achievement_id, achievement in ACHIEVEMENTS.items():
                if new_count >= achievement["smokes"]:
                    unlocked = db.unlock_achievement(
                        user_id,
                        achievement_id,
                        current_time
                    )

                    if unlocked:
                        if achievement_id == "thousand_smokes":
                            bot.reply_to(
                                message,
                                "🏆 <b>НОВЕ ДОСЯГНЕННЯ!</b>\n\n"
                                "☠️ <b>Легенда перекурів</b>\n\n"
                                "🚬 1000 перекурів.\n\n"
                                "Ми не знаємо, пишатися цим чи хвилюватися.\n"
                                "Але це сталося.",
                                parse_mode="HTML"
                            )

                        else:
                            bot.reply_to(
                                message,
                                "🏆 <b>НОВЕ ДОСЯГНЕННЯ!</b>\n\n"
                                f"{achievement['name']}\n"
                                f"{achievement['description']}",
                                parse_mode="HTML"
                            )
                        # Шанс випадіння золотої сигарети — 0.1%
                        if random.random() < 1:
                            db.add_item(
                                user_id,
                                "golden_cigarette",
                                1
                            )

                            bot.reply_to(
                                message,
                                "✨ <b>ЩО ЦЕ БУЛО?</b>\n\n"
                                "Після перекуру ти помітив щось дивне...\n\n"
                                "🚬 <b>Золота сигарета</b>\n\n"
                                "🟡 Легендарний предмет\n"
                                "🎲 Шанс випадіння: <b>0,1%</b>\n\n"
                                "Предмет додано в /inventory.",
                                parse_mode="HTML"
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