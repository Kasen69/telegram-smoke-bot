from telebot import TeleBot


def register(bot: TeleBot, db):
    
    @bot.message_handler(commands=['top'])
    def top(message):

        db.add_chat(
        message.chat.id,
        message.chat.type
        )
        ranking = db.get_top()

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