import os
import telebot
import time

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Не знайдено TOKEN у змінних середовища!")

bot = telebot.TeleBot(TOKEN)

# Зберігаємо статистику по користувачах
smokes = {}           # {user_id: count}
last_smoke_time = {}  # {user_id: timestamp}
usernames = {}        # {user_id: username}

COOLDOWN = 3600  # 1 година


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.first_name or "Без імені"

    usernames[user_id] = username

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

    usernames[user_id] = username

    current_time = time.time()

    if user_id not in smokes:
        smokes[user_id] = 0
        last_smoke_time[user_id] = 0

    if current_time - last_smoke_time[user_id] >= COOLDOWN:
        smokes[user_id] += 1
        last_smoke_time[user_id] = current_time

        bot.reply_to(
            message,
            f"✅ {username}, ти покурив!\n"
            f"🚬 Всього перекурів: {smokes[user_id]}"
        )
    else:
        remaining = int((COOLDOWN - (current_time - last_smoke_time[user_id])) / 60)

        bot.reply_to(
            message,
            f"❌ {username}, ще рано.\n"
            f"⏳ Зачекай приблизно {remaining} хв."
        )


@bot.message_handler(commands=['info'])
def info(message):
    user_id = message.from_user.id
    username = usernames.get(user_id, message.from_user.first_name or "Без імені")

    count = smokes.get(user_id, 0)

    bot.reply_to(
        message,
        f"📊 Статистика\n\n"
        f"👤 {username}\n"
        f"🚬 Перекурів: {count}\n\n"
        f"🔗 https://t.me/perekurbot69"
    )


@bot.message_handler(commands=['top'])
def top(message):
    if not smokes:
        bot.reply_to(message, "🚭 Поки що ніхто не курив.")
        return

    ranking = sorted(smokes.items(), key=lambda x: x[1], reverse=True)

    medals = ["🥇", "🥈", "🥉"]

    text = "🏆 Топ курців\n\n"

    for i, (uid, count) in enumerate(ranking[:10]):
        username = usernames.get(uid, "Без імені")

        if i < 3:
            place = medals[i]
        else:
            place = f"{i+1}."

        text += f"{place} {username} — {count}\n"

    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda m: True)
def other(message):
    text = message.text.lower()

    if text == "іді нахуй":
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