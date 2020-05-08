from threading import Thread
from datetime import datetime
import schedule
import time
import telebot
from telebot import types
import re

# pattern up to 2029 year
pattern_date = re.compile("(0[1-9])|(1[012])/([012]\d)|(3[01])/2\d:([01]\d)|(2[0-3]):[0-5]\d:[0-5]\d")
bot_token = '1021378423:AAFgThDfpte4xWsUZrkqSxk8PnIQxsU_sGs'
bot = telebot.TeleBot(bot_token)
actions = {}
action = []


@bot.message_handler(commands=['start'])
def start(mess):
    chat_id = mess.chat.id
    markup = types.ReplyKeyboardMarkup()
    button_add = types.KeyboardButton('Add action')
    button_remove = types.KeyboardButton('Remove action')
    button_remove_all = types.KeyboardButton('Remove all actions')
    button_change_name = types.KeyboardButton('Change Name your action')
    button_change_time = types.KeyboardButton('Change time your action')
    button_review = types.KeyboardButton('Review your actions')
    markup.add(button_add, button_remove, button_remove_all, button_change_name, button_change_time, button_review)
    bot.send_message(chat_id, "Hello, I'm bot which remembering you plan, choose your action ", reply_markup=markup)


@bot.message_handler(func=lambda mess: mess.text == 'Remove action' and mess.content_type == 'text')
def remove_action(mess):
    chat_id = mess.chat.id
    markup = types.ReplyKeyboardMarkup()
    echo = bot.send_message(chat_id, 'Please, type action which you would be delete!', reply_markup=markup)
    bot.register_next_step_handler(message=echo, callback=extracts_name_action)


def extracts_name_action(message):
    if message.text in actions.keys():
        actions.pop(message.text)
    else:
        bot.send_message(message.chat.id, "incorrect action, please try again write action")


@bot.message_handler(func=lambda mess: mess.text == 'Remove all actions' and mess.content_type == 'text')
def remove_all_actions(mess):
    chat_id = mess.chat.id
    markup = types.ReplyKeyboardMarkup()
    echo = bot.send_message(chat_id, 'Are you sure ?\n Write one more try yes or no ', reply_markup=markup)
    bot.register_next_step_handler(message=echo, callback=confirm_clear_dict)


def confirm_clear_dict(message):
    if (message.text == "yes") or (message.text == "Yes"):
        actions.clear()
        bot.send_message(message.chat.id, "all actions are deleted")
    elif (message.text == "no") or (message.text == "NO"):
        bot.send_message(message.chat.id, "you denied remove all")
    else:
        bot.send_message(message.chat.id, "you don't confirm remove all")


@bot.message_handler(func=lambda mess: mess.text == 'Change Name your action' and mess.content_type == 'text')
def change_action(mess):
    chat_id = mess.chat.id
    markup = types.ReplyKeyboardMarkup()
    echo = bot.send_message(chat_id, 'Write what you want change', reply_markup=markup)
    bot.register_next_step_handler(message=echo, callback=enter_action)


def enter_action(message):
    if message.text in actions.keys():
        action.extend(actions.get(message.text))
        actions.pop(message.text)
        print(action)
        echo = bot.send_message(message.chat.id, 'Write new name')
        bot.register_next_step_handler(message=echo, callback=enter_new_action)
    else:
        bot.send_message(message.chat.id, "incorrect action, please try again write action")


def enter_new_action(message):
    actions.update({message.text: [action[0], action[1]]})
    action.clear()
    bot.send_message(message.chat.id, "Your, action is successfully changed")


@bot.message_handler(func=lambda mess: mess.text == 'Change time your action' and mess.content_type == 'text')
def change_action(mess):
    chat_id = mess.chat.id
    markup = types.ReplyKeyboardMarkup()
    echo = bot.send_message(chat_id, 'Write what you want change', reply_markup=markup)
    bot.register_next_step_handler(message=echo, callback=enter_action_time)


def enter_action_time(message):
    if message.text in actions.keys():
        action.append(message.text)
        action.extend(actions.get(message.text))
        actions.pop(message.text)
        print(action)
        echo = bot.send_message(message.chat.id, 'Write new time')
        bot.register_next_step_handler(message=echo, callback=enter_new_time)
    else:
        bot.send_message(message.chat.id, "incorrect time, please try again write time")


def enter_new_time(message):
    actions.update({action[0]: [message.text, action[2]]})
    action.clear()
    bot.send_message(message.chat.id, "Your, action time is successfully changed")


@bot.message_handler(func=lambda mess: mess.text == 'Review your actions' and mess.content_type == 'text')
def review_action(mess):
    chat_id = mess.chat.id
    markup = types.ReplyKeyboardMarkup()
    bot.send_message(chat_id, 'This is your action:', reply_markup=markup)
    print(actions)
    for key in actions.keys():
        bot.send_message(chat_id, "{} - {}".format(key, actions.get(key)[0]))


@bot.message_handler(func=lambda mess: mess.text == 'Add action' and mess.content_type == 'text')
def add_action(mess):
    chat_id = mess.chat.id
    markup = types.ReplyKeyboardMarkup()
    echo = bot.send_message(chat_id, 'Please, add your action')
    bot.register_next_step_handler(message=echo, callback=extract_name_action)


def extract_name_action(message):
    action.append(message.text)

    echo = bot.send_message(message.chat.id,
                            'Please, add time of action\nPlease write time as month/day/year hh:mm:ss \n like '
                            'this:05/08/20:20:27:20')
    bot.register_next_step_handler(message=echo, callback=extract_time_action)


def extract_time_action(message):
    now = datetime.now()
    print(now)
    current_time = now.strftime("%x:%X")
    user_time = message.text
    print("Current Time =", current_time)
    print("User Time =", message.text)

    if re.match(pattern_date, message.text):
        if current_time < user_time:
            print("Ok")
            action.append(message.text)
            action.append(message.chat.id)
            actions.update({action[0]: [action[1], action[2]]})
            action.clear()
        else:
            echo = bot.send_message(message.chat.id, 'this date was in past, please write correct date')
            bot.register_next_step_handler(message=echo, callback=extract_time_action)
    else:
        echo = bot.send_message(message.chat.id, 'incorrect data, please write correct date')
        bot.register_next_step_handler(message=echo, callback=extract_time_action)


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def function_to_run():
    now = datetime.now()
    current_time = now.strftime("%x:%X")

    for key in actions.keys():
        if actions.get(key)[0] == current_time:
            bot.send_message(actions.get(key)[1], key)


schedule.every().second.do(function_to_run)
Thread(target=schedule_checker).start()
bot.polling(none_stop=True, interval=0)
