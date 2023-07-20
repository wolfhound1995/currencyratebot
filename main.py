import requests
import telebot
from telebot import types
import os
from os.path import join, dirname
from dotenv import load_dotenv
def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)
token = get_from_env('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)
def multiple(*a):
  result = 1
  for i in a:
    result = result * i
  return result

# requesting data from url
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    USDUAH = types.InlineKeyboardButton(text="USDUAH", callback_data="USDUAH")
    GBPUAH = types.InlineKeyboardButton(text="GBPUAH", callback_data="GBPUAH")
    RUBUAH = types.InlineKeyboardButton(text="RUBUAH", callback_data="RUBUAH")
    EURUAH = types.InlineKeyboardButton(text="EURUAH", callback_data="EURUAH")
    markup.add(USDUAH, RUBUAH, EURUAH, GBPUAH)
    bot.send_message(message.chat.id, 'Choose exchange currency pairs', reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = types.KeyboardButton('Back to selection')
    tip = types.KeyboardButton('Tip creator')
    markup2.add(back, tip)
    if call.data == 'USDUAH':
        key = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH"
        data = requests.get(key)
        data = data.json()
        data3price = float(data['price'])
        msg = bot.send_message(call.message.chat.id, f"{data['symbol']} price is {round(data3price, 4)} you can write your sum of USD to convert it in UAH", reply_markup=markup2)
        bot.register_next_step_handler(msg, usd_convert)
    elif call.data == 'RUBUAH':
        key = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH"
        data = requests.get(key)
        data = data.json()
        key3 = "https://api.binance.com/api/v3/ticker/price?symbol=USDTRUB"
        data4 = requests.get(key3)
        data4 = data4.json()
        data3price = (float(data['price'])/float(data4['price']))
        msg = bot.send_message(call.message.chat.id, f"RUBUAH price is {round(data3price, 3)} you can write your sum of RUB to convert it in UAH", reply_markup=markup2)
        bot.register_next_step_handler(msg, rub_convert)
    elif call.data == 'EURUAH':
        key = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH"
        data = requests.get(key)
        data = data.json()
        key3 = "https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT"
        data4 = requests.get(key3)
        data4 = data4.json()
        data3price = multiple(float(data4['price']), float(data['price']))
        msg = bot.send_message(call.message.chat.id, f"EURUAH price is {round(data3price, 3)} you can write your sum of EUR to convert it in UAH", reply_markup=markup2)
        bot.register_next_step_handler(msg, eur_convert)
    elif call.data == 'GBPUAH':
        key = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH"
        data = requests.get(key)
        data = data.json()
        key2 = "https://api.binance.com/api/v3/ticker/price?symbol=GBPUSDT"
        data3 = requests.get(key2)
        data3 = data3.json()
        data3price = multiple(float(data3['price']), float(data['price']))
        msg = bot.send_message(call.message.chat.id, f"GBPUAH price is {round(data3price, 3)} you can write your sum of GBP to convert it in UAH", reply_markup=markup2)
        bot.register_next_step_handler(msg, gbp_convert)
@bot.message_handler()
def text(message):
    if message.text == 'Tip creator':
        bot.send_message(message.chat.id, 'https://www.buymeacoffee.com//wolfhoundt6')
    elif message.text == 'Back to selection':
        start(message)
def usd_convert(message):
    user_info = message.text
    key = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH"
    data = requests.get(key)
    data = data.json()
    data3price = (float(data['price']) * float(user_info))
    bot.send_message(message.chat.id, f'Your {user_info} USD is a {data3price} UAH')
def rub_convert(message):
    user_info = message.text
    key = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH"
    data = requests.get(key)
    data = data.json()
    key3 = "https://api.binance.com/api/v3/ticker/price?symbol=USDTRUB"
    data4 = requests.get(key3)
    data4 = data4.json()
    data3price = (float(data['price']) / float(data4['price']))
    convertedrub = (float(data3price) * float(user_info))
    bot.send_message(message.chat.id, f'Your {user_info} RUB is a {round(convertedrub)} UAH')
def eur_convert(message):
    user_info = message.text
    key = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH"
    data = requests.get(key)
    data = data.json()
    key3 = "https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT"
    data4 = requests.get(key3)
    data4 = data4.json()
    data3price = multiple(float(data4['price']), float(data['price']))
    convertedeur = (float(data3price) * float(user_info))
    bot.send_message(message.chat.id, f'Your {user_info} EUR is a {convertedeur} UAH')
def gbp_convert(message):
    user_info = message.text
    key = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH"
    data = requests.get(key)
    data = data.json()
    key2 = "https://api.binance.com/api/v3/ticker/price?symbol=GBPUSDT"
    data3 = requests.get(key2)
    data3 = data3.json()
    data3price = multiple(float(data3['price']), float(data['price']))
    convertedgbp = (float(data3price) * float(user_info))
    bot.send_message(message.chat.id, f'Your {user_info} GBP is a {convertedgbp} UAH')
bot.polling(none_stop=True)