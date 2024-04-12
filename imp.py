import time
from datetime import datetime, timedelta
from resources import *
import websockets
import asyncio
import json
import bot
import re


# formating binance message
def edit_message(message):
    message = re.sub(",", ":", message)
    message = re.sub("[{}\"]", "", message)
    message = message.split(':')
    if message[0] == "result":
        return []
    return message


# formating binance traffic
async def stream_analysis(message):
    name = message[message.index('s') + 1].replace("USDT", "")
    quantity = round(float(message[message.index('q') + 1]))
    price = message[message.index('p') + 1]
    flag = message[message.index('m') + 1]
    if flag == "false":
        fill_lists(tmp_name_statistics, tmp_price_statistics, name, quantity)
        if quantity > aim:
            print("[TRADE] " + name + " " + str(quantity))
            await bot.send(message_sample.format(name, beautiful_number(str(quantity)), str(round(float(price), 5))))


# function for filling lists
def fill_lists(name_list, price_list, name, quantity):
    if name in name_list:
        index = name_list.index(name)
        price_list[index] += quantity
    else:
        name_list.append(name)
        price_list.append(quantity)


# Get data for statistics from database
def get_trade_data():
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM trade")
        all_users = curs.fetchall()
    return all_users


# Make data for statistics
def make_statistics():
    days_price.clear()
    days_name.clear()
    weeks_price.clear()
    weeks_name.clear()
    all_users = get_trade_data()
    long = len(all_users)
    now = datetime.now()
    size = len(str(now))
    day = timedelta(days=1)
    week = timedelta(weeks=1)

    for i in range(long):
        tmp_date = all_users[i][3][0:size]
        diff_date = now - datetime.strptime(tmp_date, "%Y-%m-%d %H:%M:%S.%f")
        curr = all_users[i][1].replace(" ", "")
        if diff_date <= day:
            fill_lists(days_name, days_price, curr, all_users[i][2])

        if diff_date <= week:
            fill_lists(weeks_name, weeks_price, curr, all_users[i][2])


# Add new data in database
async def fill_db():
    size = len(tmp_price_statistics)
    if size == 0:
        print("[DB][NONE]")
        return
    now = str(datetime.now())
    with conn.cursor() as curs:
        for i in range(size):
            curs.execute("INSERT INTO trade (cur, price, time) VALUES (\'{}\', {}, \'{}\')".format(
                tmp_name_statistics[i], tmp_price_statistics[i], now
            ))
            conn.commit()
    print("[DB][NEW_DATA]")
    await send_st()
    tmp_price_statistics.clear()
    tmp_name_statistics.clear()
    make_statistics()


# To send statistics to telegram
async def send_st():
    name, price = sort_data(tmp_name_statistics, tmp_price_statistics)
    res = "Статистика закупок за последний часn\n\n"
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
        res += name[i] + ": " + beautiful_number(str(price[i])) + '$\n'
    await bot.send(res)


# do every hour
async def timer():
    while True:
        await fill_db()
        await asyncio.sleep(3600)


# Connect to binance stream
async def trade():
    async with websockets.connect("wss://stream.binance.com/ws") as ws:
        await ws.send(json.dumps(upload))

        while True:
            try:
                message = await ws.recv()
            except:
                print("[ERROR][CONNECT]")
                time.sleep(5)
                continue
            message = edit_message(message)
            if not message:
                pass
            else:
                await stream_analysis(message)


async def main():
    await asyncio.gather(
        trade(),
        bot.launch_bot(),
        timer()
    )


if __name__ == '__main__':
    asyncio.run(main())
