import os
import telebot
import time
from database.database import (
    create_table,
    add_user,
    get_user,
    update_username,
    update_smoke,
    get_top,
    add_chat,
    get_user_rank,
    get_users_count,
    get_private_chats_count,
    get_group_chats_count,
    add_promo,
    get_promo,
    is_promo_used,
    use_promo,
    get_inventory,
    add_item,
)
from dotenv import load_dotenv

load_dotenv()
# Persistent volume test

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Не знайдено TOKEN у .env або змінних середовища!")

bot = telebot.TeleBot(TOKEN)

create_table()

COOLDOWN = 3600  # 1 година

ADMIN_ID = 879144294

@bot.message_handler(commands=['promo'])
def promo(message):
    user_id = message.from_user.id

    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        bot.reply_to(message, "❌ Використання:\n/promo КОД")
        return

    code = args[1].strip().upper()

    promo = get_promo(code)

    if promo is None:
        bot.reply_to(message, "❌ Такого бонус-коду не існує.")
        return

    if is_promo_used(user_id, code):
        bot.reply_to(message, "❌ Ти вже використав цей бонус-код.")
        return

    if promo["type"] == "reset_cd":
        user = get_user(user_id)

        update_smoke(
            user_id,
            user["smokes"],
            0
        )

        use_promo(user_id, code)

        bot.reply_to(
            message,
            "🎉 Бонус-код активовано!\n"
            "⏳ Час очікування скинуто."
        )

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.first_name or "Без імені"

    add_chat(
    message.chat.id,
    message.chat.type
    )

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
        "/top — топ курців\n"
    )

@bot.message_handler(commands=['smoke'])
def smoke(message):
    user_id = message.from_user.id
    username = message.from_user.first_name or "Без імені"

    add_chat(
    message.chat.id,
    message.chat.type
    )

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
            f"🚬 Всього перекурів : {new_count}"
        )

    else:
        remaining_seconds = int(
            COOLDOWN - (current_time - user["last_smoke"])
        )

        if remaining_seconds >= 300:  # 5 хвилин
            minutes = remaining_seconds // 60
            wait_time = f"{minutes} хв"

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


@bot.message_handler(commands=['info'])
def info(message):
    user_id = message.from_user.id

    add_chat(
    message.chat.id,
    message.chat.type
    )
    user = get_user(user_id)

    if user is None:
        bot.reply_to(message, "У тебе ще немає статистики.")
        return

    username = user["username"]
    count = user["smokes"]

    rank = get_user_rank(user_id)

    bot.reply_to(
    message,
    f"📊 Статистика\n\n"
    f"👤 {username}\n"
    f"🚬 Перекурів: {count}\n"
    f"🏆 Місце в топі: #{rank}\n\n"
    f"🔗 https://t.me/perekurbot69"
)


@bot.message_handler(commands=['top'])
def top(message):
    add_chat(
    message.chat.id,
    message.chat.type
    )
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
    private_chats = get_private_chats_count()
    groups = get_group_chats_count()

    bot.reply_to(
        message,
        f"📊 Статистика бота\n\n"
        f"👥 Користувачів: {users}\n"
        f"👤 Особистих чатів: {private_chats}\n"
        f"👥 Груп: {groups}"
    )


@bot.message_handler(commands=['inventory'])
def inventory(message):
    user_id = message.from_user.id

    add_chat(
        message.chat.id,
        message.chat.type
    )

    items = get_inventory(user_id)

    if not items:
        bot.reply_to(
            message,
            "🎒 Інвентар порожній."
        )
        return

    text = "🎒 Твій інвентар\n\n"

    for item in items:
        text += f"• {item['item_name']} ×{item['amount']}\n"

    bot.reply_to(message, text)

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



#Це має бути останнім!



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
