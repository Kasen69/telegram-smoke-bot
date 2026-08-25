from telebot import TeleBot
from items.items import ITEMS

ADMIN_ID = 879144294

def register(bot: TeleBot, db):
    @bot.message_handler(commands=['give'])
    def give(message):
        
        if message.from_user.id != ADMIN_ID:
            return

        items_list = "\n".join([f"• `{item_id}` — {info['name']}" for item_id, info in ITEMS.items()])
        usage_text = (
            f"❌ **Використання:**\n`/give [ID користувача] [ID предмета] [кількість]`\n\n"
            f"📦 **Доступні предмети:**\n{items_list}"
        )

        args = message.text.split()
        
        if len(args) != 4:
            bot.reply_to(message, usage_text, parse_mode="Markdown")
            return

        try:
            user_id = int(args[1])
            item = args[2].lower()
            amount = int(args[3])
        except ValueError:
            bot.reply_to(message, "❌ **Помилка:** ID та кількість повинні бути числами.", parse_mode="Markdown")
            return

        if item not in ITEMS:
            bot.reply_to(message, f"❌ **Помилка:** Предмета `{item}` не існує.\n\n{usage_text}", parse_mode="Markdown")
            return

        if amount <= 0:
            bot.reply_to(message, "❌ **Помилка:** Кількість повинна бути більшою за 0.", parse_mode="Markdown")
            return

        db.add_item(user_id, item, amount)
        
        item_name = ITEMS[item]['name']
        bot.reply_to(
            message, 
            f"✅ Користувачу `{user_id}` успішно видано **{item_name}** ({amount} шт.).", 
            parse_mode="Markdown"
        )