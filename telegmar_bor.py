from datetime import datetime

import schedule
import time

import telebot
from telebot import types
import shelve

import sqlite3

conn = sqlite3.connect('information3.db')
c = conn.cursor()

# c.execute('''CREATE TABLE information10
#             (chat_id text, task text, time text)''')

bot_token = '1021378423:AAFgThDfpte4xWsUZrkqSxk8PnIQxsU_sGs'
bot = telebot.TeleBot(bot_token)
actions = {}
action = []

durak = False


# ssssss
@bot.message_handler(commands=['start'])
def start(mess):
    chat_id = mess.chat.id
    db = shelve.open('shelve')
    db[str(chat_id)] = 'init'
    db.close()

    markup = types.ReplyKeyboardMarkup()
    btn_a = types.KeyboardButton('Add action')
    btn_b = types.KeyboardButton('Delete action')
    btn_c = types.KeyboardButton('Remove all action')
    btn_d = types.KeyboardButton('Change your action')
    btn_e = types.KeyboardButton('Review your action')
    btn_f = types.KeyboardButton('ЩОТЧИК')
    markup.add(btn_a, btn_b, btn_c, btn_d, btn_e, btn_f)
    bot.send_message(chat_id,
                     "Hello, I'm bot which remembering you plan, choose your "
                     "action ",
                     reply_markup=markup)



@bot.message_handler(func=lambda
        mess: mess.text == 'Delete action' and mess.content_type == 'text')
def b(mess):
    chat_id = mess.chat.id
    db = shelve.open('shelve')
    state = db[str(chat_id)]
    if state != 'init':
        start(mess)
    else:
        # db[str(chat_id)] = 'Delete action'
        db.close()
        markup = types.ReplyKeyboardMarkup()
        bot.send_message(chat_id,
                         'Please, type action which you would be delete!',
                         reply_markup=markup)


@bot.message_handler(func=lambda mess: mess.text == 'Remove all action' and
                                       mess.content_type == 'text')
def c(mess):
    chat_id = mess.chat.id
    db = shelve.open('shelve')
    state = db[str(chat_id)]
    if state != 'init':
        start(mess)
    else:
        # db[str(chat_id)] = 'Remove all action'
        db.close()
        markup = types.ReplyKeyboardMarkup()
        bot.send_message(chat_id, 'Are you sure ?\n Write one more try yes or no ', reply_markup=markup)


@bot.message_handler(
    func=lambda mess: mess.text == 'Change your action' and
                      mess.content_type == 'text')
def d(mess):
    chat_id = mess.chat.id
    db = shelve.open('shelve')
    state = db[str(chat_id)]
    if state != 'init':
        start(mess)
    else:
        # db[str(chat_id)] = 'Change your action'
        db.close()
        markup = types.ReplyKeyboardMarkup()
        bot.send_message(chat_id, 'Write what you want change',
                         reply_markup=markup)


@bot.message_handler(func=lambda mess: mess.text == 'Review your action' and mess.content_type == 'text')
def e(mess):
    chat_id = mess.chat.id
    db = shelve.open('shelve')
    state = db[str(chat_id)]
    if state != 'init':
        start(mess)
    else:
        # db[str(chat_id)] = 'Review your action'
        db.close()
        markup = types.ReplyKeyboardMarkup()
        bot.send_message(chat_id, 'This is your action', reply_markup=markup)
        print(actions)
        for key in actions.keys():
            bot.send_message(chat_id, "{} - {}".format(key, actions.get(key)))


@bot.message_handler(func=lambda mess: mess.text == 'ЩОТЧИК' and
                                       mess.content_type == 'text')
def f(mess):
    chat_id = mess.chat.id
    db = shelve.open('shelve')
    state = db[str(chat_id)]
    if state != 'init':
        start(mess)
    else:
        # db[str(chat_id)] = 'Remove all action'
        durak = True
        db.close()


@bot.message_handler(func=lambda mess: mess.text == 'Add action' and
                                       mess.content_type == 'text')
def a(mess):
    chat_id = mess.chat.id
    db = shelve.open('shelve')
    state = db[str(chat_id)]
    if state != 'init':
        start(mess)
        return
        # db[str(chat_id)] = 'Add action'
    db.close()
    markup = types.ReplyKeyboardMarkup()

    echo = bot.send_message(chat_id, 'Please, add your action')
    bot.register_next_step_handler(message=echo, callback=extract_name_action)


def extract_name_action(message):
    action.append(message.text)
    user_action = message.text
    echo = bot.send_message(message.chat.id,
                            'Please, add time of action\nPlease write time as day/month/year hh:mm:ss')

    bot.register_next_step_handler(message=echo, callback=extract_time_action)


def extract_time_action(message):
    user_time = message.text
    now = datetime.now()
    current_time = now.strftime("%x:%X")
    print("Current Time =", current_time)

    if int(current_time[0:2]) > int(user_time[0:2]):
        print("incorrect data")
        bot.send_message(message.chat.id, 'incorrect data')
        return

    if int(current_time[0:2]) == int(user_time[0:2]):
        if int(current_time[3:5]) > int(user_time[3:5]):
            print("incorrect data")
            bot.send_message(message.chat.id, 'incorrect data')
            return

    if int(current_time[0:2]) == int(user_time[0:2]):
        if int(current_time[3:5]) == int(user_time[3:5]):
            if int(current_time[6:8]) > int(user_time[6:8]):
                print("incorrect data")
                bot.send_message(message.chat.id, 'incorrect data')
                return

    if int(current_time[0:2]) == int(user_time[0:2]):
        if int(current_time[3:5]) == int(user_time[3:5]):
            if int(current_time[6:8]) == int(user_time[6:8]):
                if int(current_time[9:11]) > int(user_time[9:11]):
                    print("incorrect data")
                    bot.send_message(message.chat.id, 'incorrect data')
                    return

    if int(current_time[0:2]) == int(user_time[0:2]):
        if int(current_time[3:5]) == int(user_time[3:5]):
            if int(current_time[6:8]) == int(user_time[6:8]):
                if int(current_time[9:11]) == int(user_time[9:11]):
                    if int(current_time[12:14]) > int(user_time[12:14]):
                        print("incorrect data")
                        bot.send_message(message.chat.id, 'incorrect data')
                        return

    if int(current_time[0:2]) == int(user_time[0:2]):
        if int(current_time[3:5]) == int(user_time[3:5]):
            if int(current_time[6:8]) == int(user_time[6:8]):
                if int(current_time[9:11]) == int(user_time[9:11]):
                    if int(current_time[12:14]) == int(user_time[12:14]):
                        if int(current_time[15:17]) > int(user_time[15:17]):
                            print("incorrect data")
                            bot.send_message(message.chat.id, 'incorrect data')
                            return

    print("good")
    print(message.text)
    action.append(message.text)
    actions.update({action[0]: action[1]})
    action.clear()
    print("end function")
    lox = True
    #   def job():

    while durak:
        time.sleep(1)
        now = datetime.now()
        current_time = now.strftime("%x:%X")
        #        print(current_time)
        for key in actions.keys():
            if actions.get(key) == current_time:
                #         print("sadadassd")
                bot.send_message(message.chat.id, key)
                lox = False
                break


#    schedule.every(1).seconds.do(job)
#    schedule.run_pending()


#        schedule.run_pending()
#        time.sleep(1)


# 05/07/20:21:27:20


bot.polling(none_stop=True, interval=0)
