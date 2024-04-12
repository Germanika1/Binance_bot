import aiogram.exceptions
from aiogram import *
from aiogram.filters import CommandStart
from resources import *

bot = Bot(token=TOKEN)
dp = Dispatcher()


button_1 = types.KeyboardButton(text="Статистика")
menu_buttons = [[button_1]]
menu = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=menu_buttons)


# add user id in database
def add_id(user_id):
    with conn.cursor() as curs:
        curs.execute("INSERT INTO users (value) VALUES ({})".format(user_id))
        conn.commit()
    print("[LOG][ADD_ID] ---> ", user_id)


# get all users from database
def get_users():
    with conn.cursor() as curs:
        curs.execute("SELECT value FROM users")
        all_users = curs.fetchall()
    result = [all_users[i][0] for i in range(len(all_users))]
    return result


# what to do with user id
def define_id(user_id):
    result = get_users()
    if user_id not in result:
        add_id(user_id)


# Message /start
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    define_id(message.chat.id)
    await message.answer(text="""
Добро пожаловать \U0001F525\nВам будут приходить сообщения с большими закупками различных валют \U0001F680""", reply_markup=menu)


# Send week and day statistic
@dp.message(F.text.lower() == "статистика")
async def statistics_handler(message: types.Message):
    named, priced = sort_data(days_name, days_price)
    name_w, price_w = sort_data(weeks_name, weeks_price)
    res = "Статистика закупок за сутки \U0001F3EB\n\n"
    if len(priced) < 5 or len(price_w) < 5:
        await message.answer(text="Подождите, данные собираются", reply_markup=menu)
        return
    for i in range(5):
        if i == 0:
            res += "\U0001F947"
        elif i == 1:
            res += "\U0001F948"
        elif i == 2:
            res += "\U0001F949"
        elif i == 3:
            res += "\U0001F396"
        else:
            res += "\U0001F3C5"
        res += named[i] + ": " + beautiful_number(str(priced[i])) + '$\n'

    res += "\nСтатистика за неделю \U0001F4C6\n\n"
    for i in range(5):
        if i == 0:
            res += "\U0001F947"
        elif i == 1:
            res += "\U0001F948"
        elif i == 2:
            res += "\U0001F949"
        elif i == 3:
            res += "\U0001F396"
        else:
            res += "\U0001F3C5"
        res += name_w[i] + ": " + beautiful_number(str(price_w[i])) + '$\n'
    await message.answer(text=res, reply_markup=menu)


# function for sending messages
async def send(message):
    ids = get_users()
    for i in range(len(ids)):
        try:
            await bot.send_message(ids[i], message)
        except aiogram.exceptions.TelegramForbiddenError:
            print("[BLOCKED] ", ids[i])
        except aiogram.exceptions.TelegramBadRequest:
            print("[ID BLOCKED]", ids[i])


async def launch_bot():
    await dp.start_polling(bot)
