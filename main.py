import logging
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ApplicationBuilder
import sqlite3
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# WARNING fill this part
CHANNEL_ID = ""
TOKEN = ""
DB_NAME= "memes.db"

con = sqlite3.connect(DB_NAME)
c = con.cursor()
global post

# Send a media if accepted support gif and pics(not a command function)
async def send_media(url, caption, context, update, sendTo):
    gif_format = ['gif', 'giv']
    pic_format = ['png', 'jpg']

    x = url.split('.')[-1]
    if x in gif_format:
        try:
            await context.bot.send_animation(chat_id=sendTo, animation=post[4], caption=caption)
        except:
            pass

    if x in pic_format:
        try:
            await context.bot.send_photo(chat_id=sendTo, photo=post[4], caption=caption)
        except:
            pass

# start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[KeyboardButton('/post')]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!",
                                   reply_markup=ReplyKeyboardMarkup(buttons))

# show a post and asks for approve
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global post
    c.execute("""SELECT * FROM meme WHERE pub=0 ORDER BY score DESC""")
    post = c.fetchone()
    keyboard = [
        [
            InlineKeyboardButton("cool", callback_data="1"),
        ],
        [InlineKeyboardButton("uncool", callback_data="2")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # await context.bot.send_photo(chat_id=update.effective_chat.id,photo=post[4],caption=post[1])
    print(post[4]+post[1])
    # await context.bot.send_animation(chat_id=update.effective_chat.id,animation=post[4],caption=post[1])
    await send_media(post[4], post[1], context, update, sendTo=update.effective_user.id)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def queryHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query.data
    await update.callback_query.answer()
    global post
    if "1" in query:
        c.execute(f"""UPDATE meme SET pub =1 WHERE id='{post[0]}'""")
        con.commit()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="okay")
        caption = f"{post[1]}\n\n {CHANNEL_ID}"
        await send_media(post[4], caption, context, update, sendTo=CHANNEL_ID)
        # await context.bot.send_photo(photo=post[4],chat_id=CHANNEL_ID,caption=f"{post[1]}\n\n {CHANNEL_ID}")
    if "2" in query:
        c.execute(f"""UPDATE meme SET pub =2 WHERE id='{post[0]}'""")
        con.commit()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="okay virgin")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    post_handler = CommandHandler('post', post)
    application.add_handler(post_handler)

    application.add_handler(CallbackQueryHandler(queryHandler))
    application.run_polling()
