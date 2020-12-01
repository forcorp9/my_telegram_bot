from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.joinpath('files')


# print(BASE_DIR)
#D:\python_kurs\tg_bots\src\main.py
#D:\python_kurs\tg_bots\files
# D:\python_kurs\tg_bots\files
from telegram.ext import (
    CommandHandler,
    Updater,
    Filters,
    CallbackContext,
    ConversationHandler,
    MessageHandler, CallbackQueryHandler
)
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from db_helper import DbHelper

db = DbHelper()

def start(update: Update, context: CallbackContext):
    from_user = update.message.from_user
    user = db.getUserById(from_user.id)
    if not user:
        db.createUser(from_user.id, from_user.username, from_user.first_name)

    categories = db.getCategories()


    if categories:
        buttons = generateButtons(categories)
    else:
        buttons = []


    update.message.reply_text(
        'Assalomu alaykum.\nKategoriyalardan birini tanlang: ',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return 2

def update_catalog(update, context):
    query = update.callback_query
    datas = query.data.split('_')

    if datas[0] == 'category':
        cat_id = int(datas[1])
        childs = db.getCategorychilds(cat_id)
        if childs:
            buttons = generateButtons(childs)
            query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))
        else:
            product = db.getproductByCategory_id(cat_id)
            tx = f"<b>{product['name']}</b>\n \nNarxi:{product['amount']} so`m"
            # query.edit_message_text(tx, parse_mode="HTML")
            file_path = BASE_DIR.joinpath(product['file_path'])
            # print(file_path)
            # query.edit_message_(tx, parse_mode="HTML")
            context.user_data['product_id'] = product['id']
            buttons = generateNumButtons()
            query.message.delete()
            query.message.reply_photo(open(file_path, 'rb'),
            caption=tx, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))
    elif datas[0] == 'number':
        num = int(datas[1])
        product_id = int(context.user_data['product_id'])
        product = db.getproductById(product_id)
        sum = int(product['amount']) * num

        txt = f"<b>В корзине:</b>\n \n{num}⃣ ✖️{product['name']}\n \n<b>Товары:</b>    {sum} сум"

        query.message.delete()
        query.message.reply_text(txt, parse_mode="HTML")


def error(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Xatolik'
    )

def generateButtons(categories):
    buttons = []
    tmp_buttons = []
    for category in categories:
        tmp_buttons.append(
            InlineKeyboardButton(category['name'],
            callback_data=f'category_{category["id"]}')
        )
        if len(tmp_buttons) == 2:
            buttons.append(tmp_buttons)
            tmp_buttons = []
    if len(tmp_buttons) > 0:
        buttons.append(tmp_buttons)

    return buttons

def generateNumButtons():
    buttons = []
    tmp_buttons = []
    for num in range(1, 10):
        tmp_buttons.append(
            InlineKeyboardButton(str(num),
            callback_data=f'number_{num}')
        )
        if len(tmp_buttons) == 3:
            buttons.append(tmp_buttons)
            tmp_buttons = []

    return buttons


updater = Updater("1012930685:AAFpnI_BNrlSzIPHIr6i5o68dbax7F-7jBE", use_context=True)
dispatcher = updater.dispatcher

# dispatcher.add_handler(CommandHandler('start', start))


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        2: [CallbackQueryHandler(update_catalog)]

    },
    fallbacks=[CommandHandler('cancel', error)],
)
dispatcher.add_handler(conv_handler)


updater.start_polling()
updater.idle()
