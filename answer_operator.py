import telebot
import random
import text
import time

from config import allowed_channels
from random import randint
from telebot import types

from text import (call_name,
                  call_aderes,
                  call_victims,
                  text_menu,
                  text_when_call,
                  call_situation,
                  text_members_emergency,
                  leaved)


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    help_button = types.InlineKeyboardButton(text='Экстренные службы', callback_data='help')
    quiz_button = types.InlineKeyboardButton(text='У меня есть вопрос', callback_data='quiz')
    exit_button = types.InlineKeyboardButton(text='Извините, я ошибся номером', callback_data='exit')

    keyboard.add(help_button)
    keyboard.add(quiz_button)
    keyboard.add(exit_button)

    return keyboard


def callback_query(call: types.CallbackQuery, bot: telebot.TeleBot):
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == 'help':
        keyboard_emergency = types.InlineKeyboardMarkup()
        police = types.InlineKeyboardButton(text='Полиция', callback_data='pd')
        ems = types.InlineKeyboardButton(text='Медики', callback_data='ems')
        fd = types.InlineKeyboardButton(text='Пожарные', callback_data='fd')

        keyboard_emergency.add(police)
        keyboard_emergency.add(ems)
        keyboard_emergency.add(fd)

        with open("image/emergency.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, random.choice(text_members_emergency),
                           reply_markup=keyboard_emergency)

    elif call.data == "pd":
        emergency = "полиции"
        with open("image/police.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=random.choice(call_name))
        bot.register_next_step_handler(call.message, lambda msg: process_name_step(bot, msg, emergency))

    elif call.data == "ems":
        emergency = "состава медиков"
        with open("image/medic.png", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=random.choice(call_name))
        bot.register_next_step_handler(call.message, lambda msg: process_name_step(bot, msg, emergency))

    elif call.data == "fd":
        emergency = "пожарного департамента"
        with open("image/fierman.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=random.choice(call_name))
        bot.register_next_step_handler(call.message, lambda msg: process_name_step(bot, msg, emergency))

    elif call.data == "quiz":
        keyboard_quiz = types.InlineKeyboardMarkup()
        how_long = types.InlineKeyboardButton(text='Сколько времени нужно ждать помощь?', callback_data='how_long')
        hard_job = types.InlineKeyboardButton(text='Сложно ли вам работать в 911?', callback_data='hard_job')
        how_join_police = types.InlineKeyboardButton(text='Как можно устроиться в полицию?',
                                                     callback_data='how_join_police')

        keyboard_quiz.add(how_long)
        keyboard_quiz.add(hard_job)
        keyboard_quiz.add(how_join_police)

        bot.send_message(call.message.chat.id, "Какой вопрос вы хотите задать?:", reply_markup=keyboard_quiz)

    elif call.data == "how_long":
        bot.send_message(call.message.chat.id, text.how_long)

    elif call.data == "hard_job":
        bot.send_message(call.message.chat.id, text.hard_job)

    elif call.data == "how_join_police":
        bot.send_message(call.message.chat.id, text.how_join_police)

    elif call.data == "exit":
        bot.send_message(call.message.chat.id, leaved)  # Добавим обратную связь


def process_name_step(bot: telebot.TeleBot, message: telebot.types.Message, emergency):
    name = message.text
    bot.send_message(message.chat.id, random.choice(call_aderes))
    bot.register_next_step_handler(message, lambda msg: process_address_step(bot, msg, emergency, name))


def process_address_step(bot: telebot.TeleBot, message: telebot.types.Message, emergency, name):
    address = message.text
    bot.send_message(message.chat.id, random.choice(call_situation))
    bot.register_next_step_handler(message, lambda msg: process_situation_step(bot, msg, emergency, name, address))


def process_situation_step(bot: telebot.TeleBot, message: telebot.types.Message, emergency, name, address):
    situation = message.text
    bot.send_message(message.chat.id, random.choice(call_victims))
    bot.register_next_step_handler(message, lambda msg: process_victims_step(bot, msg, emergency, name, address, situation))


def process_victims_step(bot: telebot.TeleBot, message: telebot.types.Message, emergency, name, address, situation):
    victims = message.text
    user_id = message.from_user.id

    bot.send_message(allowed_channels,f"""
    Всем сотрудникам {emergency}, только что поступил вызов!\n
    Пострадавший: {name}  ->  номер в безе данных: ({user_id})
    Находится по адресу  ->  {address}\n
    Описание ситуации:  {situation}
    Количесто жертв: {victims}
    """)
    bot.send_message(message.chat.id, "Хорошо, помощь уже в пути, остовайтесь на месте.")


def start_prt(message: telebot.types.Message, bot: telebot.TeleBot):
    markup = create_keyboard()
    for _ in range(1, 3):
        bot.send_message(message.chat.id, text_when_call[_])
        time.sleep(randint(1, 3))
    with open("image/menu/bot_menu.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, random.choice(text_menu), reply_markup=markup)
