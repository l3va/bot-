import schedule
import telebot
from threading import Thread
from time import sleep

TOKEN = '1021378423:AAFgThDfpte4xWsUZrkqSxk8PnIQxsU_sGs'

bot = telebot.TeleBot(TOKEN)

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

@bot.message_handler(commands=['start'])
def test_send_message(message):
    tb = telebot.TeleBot(TOKEN)
    ret_msg = tb.send_message(message.chat.id, 'hello')
    assert ret_msg.message_id

if current_time == '11:01:00':
 test_send_message()

bot.polling()