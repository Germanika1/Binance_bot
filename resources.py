import psycopg2


currency = [
    "sntusdt@aggTrade",
    "powrusdt@aggTrade",
    "joeusdt@aggTrade",
    "arkusdt@aggTrade",
    "auctionusdt@aggTrade",
    "hookusdt@aggTrade",
    "bakeusdt@aggTrade",
    "highusdt@aggTrade",
    "vrausdt@aggTrade",
    "dorausdt@aggTrade",
    "fttusdt@aggTrade",
    "algousdt@aggTrade",
    "kasusdt@aggTrade",
    "darusdt@aggTrade",
    "audiousdt@aggTrade",
    "blzusdt@aggTrade",
    "ondousdt@aggTrade",
    "mavusdt@aggTrade",
    "jupusdt@aggTrade",
    "storjusdt@aggTrade",
    "arpausdt@aggTrade",
    "celrusdt@aggTrade",
    "pendleusdt@aggTrade",
    "ldousdt@aggTrade",
    "jtousdt@aggTrade",
    "sandusdt@aggTrade",
    "manausdt@aggTrade",
    "taousdt@aggTrade",
    "laiusdt@aggTrade",
    "perpusdt@aggTrade",
    "hifiusdt@aggTrade",
    "roseusdt@aggTrade",
    "opusdt@aggTrade",
    "oneusdt@aggTrade",
    "zrxusdt@aggTrade",
    "woousdt@aggTrade",
    "trxusdt@aggTrade",
    "eosusdt@aggTrade",
    "synusdt@aggTrade",
    "wifusdt@aggTrade",
    "portalusdt@aggTrade",
    "lskusdt@aggTrade",
    "lunausdt@aggTrade",
    "ensusdt@aggTrade",
    "icpusdt@aggTrade",
    "nearusdt@aggTrade",
    "aptusdt@aggTrade",
    "tiausdt@aggTrade",
    "arbusdt@aggTrade",
    "fetusdt@aggTrade",
    "seiusdt@aggTrade"
    "aaveusdt@aggTrade",
    "flowusdt@aggTrade",
    "ordiusdt@aggTrade",
    "egldusdt@aggTrade",
    "runeusdt@aggTrade",
    "strkusdt@aggTrade",
    "astusdt@aggTrade",
    "dfusdt@aggTrade",
    "uftusdt@aggTrade",
    "pntusdt@aggTrade",
    "cvpusdt@aggTrade",
    "vibusdt@aggTrade",
    "oaxusdt@aggTrade",
    "drepusdt@aggTrade",
    "atmusdt@aggTrade",
    "asrusdt@aggTrade",
    "movrusdt@aggTrade",
    "yggusdt@aggTrade",
    "polyxusdt@aggTrade",
]

conn = psycopg2.connect(dbname="TheCCbot", user="postgres", password="berlad123", host="localhost")
cursor = conn.cursor()

tmp_price_statistics = []
tmp_name_statistics = []

days_name = []
days_price = []
weeks_name = []
weeks_price = []

TOKEN = "6854386059:AAGj7S94A8Pr1MQ0Er7sVVLnSWFx-YfppC4"

aim = 100000

upload = {
        "id": 1,
        "method": "SUBSCRIBE",
        "params": currency
}

message_sample = """
\U0001F54B Рынок: SPOT
\U0001F4F0 Валюта: {}
\U0001F4B0 Сделка: {}$
\U0001F4B5 Цена валюты: {}$"""


def beautiful_number(num):
    res = ""
    num = num[::-1]
    for i in range(0, len(num), 3):
        res += num[i: i + 3] + '.'
    res = res[::-1]
    return res[1::]


def sort_data(nm, pr):
    price = pr.copy()
    name = nm.copy()
    long = len(price)
    for i in range(long):
        for k in range(1, long):
            if price[k] > price[k - 1]:
                price[k], price[k - 1] = price[k - 1], price[k]
                name[k], name[k - 1] = name[k - 1], name[k]
    return name, price
