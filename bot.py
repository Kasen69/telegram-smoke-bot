import os
import telebot
import time
from database import (
    create_table,
    add_user,
    get_user,
    update_username,
    update_smoke,
    get_top,
)
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Не знайдено TOKEN у .env або змінних середовища!")

bot = telebot.TeleBot(TOKEN)

create_table()

COOLDOWN = 3600  # 1 година

ADMIN_ID = 879144294

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.first_name or "Без імені"

    add_chat(message.chat.id)

    user = get_user(user_id)

    if user is None:
        add_user(user_id, username)

    update_username(user_id, username)

    bot.send_message(
        message.chat.id,
        "🚬 Привіт! Я бот-рахівник перекурів.\n\n"
        "Команди:\n"
        "/smoke — покурити\n"
        "/info — твоя статистика\n"
        "/top — топ курців"
    )


@bot.message_handler(commands=['smoke'])
def smoke(message):
    user_id = message.from_user.id
    username = message.from_user.first_name or "Без імені"

    add_chat(message.chat.id)

    current_time = time.time()

    user = get_user(user_id)

    if user is None:
        add_user(user_id, username)

    update_username(user_id, username)
    user = get_user(user_id)

    if current_time - user["last_smoke"] >= COOLDOWN:
        new_count = user["smokes"] + 1

        update_smoke(
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
        remaining = int((COOLDOWN - (current_time - user["last_smoke"])) / 60)

        bot.reply_to(
            message,
            f"❌ {username}, ще рано.\n"
            f"⏳ Зачекай приблизно {remaining} хв."
        )


@bot.message_handler(commands=['info'])
def info(message):
    user_id = message.from_user.id

    add_chat(message.chat.id)
    user = get_user(user_id)

    if user is None:
        bot.reply_to(message, "У тебе ще немає статистики.")
        return

    username = user["username"]
    count = user["smokes"]

    bot.reply_to(
        message,
        f"📊 Статистика\n\n"
        f"👤 {username}\n"
        f"🚬 Перекурів: {count}\n\n"
        f"🔗 https://t.me/perekurbot69"
    )


@bot.message_handler(commands=['top'])
def top(message):
    add_chat(message.chat.id)
    ranking = get_top()

    if len(ranking) == 0:
        bot.reply_to(message, "🚭 Поки що ніхто не курив.")
        return

    medals = ["🥇", "🥈", "🥉"]

    text = "🏆 Топ курців\n\n"

    for i, user in enumerate(ranking):
        username = user["username"]
        count = user["smokes"]

        if i < 3:
            place = medals[i]
        else:
            place = f"{i+1}."

        text += f"{place} {username} — {count}\n"

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id != ADMIN_ID:
        return

    users = get_users_count()
    chats = get_chats_count()

    bot.reply_to(
        message,
        f"📊 Статистика бота\n\n"
        f"👥 Користувачів: {users}\n"
        f"💬 Чатів: {chats}"
    )

@bot.message_handler(func=lambda m: True)
def other(message):
    text = message.text.lower()

    if "іді нахуй" in text and "@pitpivo69bot" in text:
        bot.reply_to(message, "сам іді")

    elif text == "іді нахуй":
        bot.reply_to(message, "сам іді")

    elif text == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")


while True:
    try:
        print("Бот запущений...")
        bot.infinity_polling(timeout=30, long_polling_timeout=10)
    except Exception as e:
        print(e)
        print("Перезапуск через 5 секунд...")
        time.sleep(5)
