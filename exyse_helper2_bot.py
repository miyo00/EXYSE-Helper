import re
import logging
import os
from datetime import timedelta
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN =os.getenv(8197294780:AAE59ZsyrPsY8h8nfnIDAoYKYtwRRkAICmo)

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❗ Відповідай на повідомлення користувача, якого хочеш забанити.")
        return

    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.effective_chat.id

    logging.info(f"Спроба забанити користувача {user_id} в чаті {chat_id}")

    try:
        await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
        await update.message.reply_text("✅ Користувач забанений.")
    except Exception as e:
        logging.error(f"Помилка при бані: {e}")
        await update.message.reply_text(f"❌ Помилка при бані: {e}")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❗ Відповідай на повідомлення користувача, якого хочеш розбанити.")
        return

    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.effective_chat.id

    logging.info(f"Спроба розбанити користувача {user_id} в чаті {chat_id}")

    try:
        await context.bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
        await update.message.reply_text("🔓 Користувач розбанений.")
    except Exception as e:
        logging.error(f"Помилка при розбані: {e}")
        await update.message.reply_text(f"❌ Помилка при розбані: {e}")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❗ Відповідай на повідомлення користувача, якого хочеш зам'ютити.\nПриклад: /mute 10m")
        return

    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Вкажи час м'юту. Приклад: /mute 10m або /mute 1h")
        return

    time_str = context.args[0]
    m = re.match(r"(\d+)([mh])", time_str)
    if not m:
        await update.message.reply_text("❌ Невірний формат часу. Використовуй 10m або 1h.")
        return

    num, unit = int(m[1]), m[2]
    duration = timedelta(minutes=num) if unit == "m" else timedelta(hours=num)

    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.effective_chat.id

    logging.info(f"Спроба зам'ютити користувача {user_id} на {duration}")

    try:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=update.message.date + duration
        )
        await update.message.reply_text(f"🔇 Користувач зам'ючений на {num}{unit}.")
    except Exception as e:
        logging.error(f"Помилка при м'юті: {e}")
        await update.message.reply_text(f"❌ Помилка при м'юті: {e}")

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❗ Відповідай на повідомлення користувача, якого хочеш розм'ютити.")
        return

    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.effective_chat.id

    logging.info(f"Спроба розм'ютити користувача {user_id}")

    try:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await update.message.reply_text("🔊 Користувач розм'ючений.")
    except Exception as e:
        logging.error(f"Помилка при розм'юті: {e}")
        await update.message.reply_text(f"❌ Помилка при розм'юті: {e}")

async def show_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = (
        "*Правила чата:*\n\n"
        "*1. Забороняється фото/відео/текст 18+ контенту*\n"
        "1.1 У чатах компанії забороняється 18+ контент у будь-якій формі. До чатів компанії відносяться: чат трейні, спільний чат, чат стаффу, чат гурту.\n"
        "*2. Підтримка країни агресора*\n"
        "2.1 Забороняється використовувати російські емоджі/гіф/стікери. До них відносяться: емоджі/гіф/стікери з текстом на російській мові, емоджі/гіф з російською мовою в назві, або посиланням на російськомовний канал.\n"
        "2.2 Забороняються кавери та практики на пісні російських співаків. Але дозволяється робити переклади, якщо це український гурт/співак.\n"
        "*3. Спам*\n"
        "3.1 Спам забороняється в усіх чатах компанії. До чатів компанії відносяться: чат трейні, спільний чат, чат стаффу, чат гурту.\n"
        "*4. Конфлікти*\n"
        "4.1 Конфлікти в чатах компанії заборонено. Якщо стався конфлікт — відмічайте директорів або пишіть їм. До чатів компанії відносяться: чат трейні, спільний чат, чат стаффу, чат гурту.\n"
        "*5. Реклама в чаті, без дозволу хочаб одного з директорів*\n"
        "5.1 Реклама каналів в чатах компанії заборонена. До чатів компанії відносяться: чат трейні, спільний чат, чат стаффу, чат гурту.\n"
        "5.2 Дозволяється реклама каналів, які відносяться до нашої компанії.\n"
        "*6. Ліміт компаній та гуртів*\n"
        "6.1 Встановлено ліміт на 1 компанію окрім нашої. Тобто ви можете перебувати в 2 компаніях, в нашій та ще одній.\n"
        "6.2 Встановлено ліміт на 1 гурт без компанії. Тобто ви можете перебувати в нашій компанії та в гурті без компанії.\n"
    )
    await update.message.reply_text(rules_text, parse_mode="Markdown")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("ban", ban_user))
app.add_handler(CommandHandler("unban", unban_user))
app.add_handler(CommandHandler("mute", mute_user))
app.add_handler(CommandHandler("unmute", unmute_user))
app.add_handler(CommandHandler("rules", show_rules))

print("Бот запущено.")
app.run_polling()
