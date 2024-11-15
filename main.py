import answer_operator
import threading
import telebot
import config


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["call", "911", "112"])
def say_start(message: telebot.types.Message):
    answer_operator.start_prt(message, bot)


@bot.callback_query_handler(func=lambda call: True)
def say_prise(call: telebot.types.CallbackQuery):
    threading.Thread(target=lambda: answer_operator.callback_query(call, bot)).start()


if __name__ == "__main__":
    bot.polling(none_stop=True)
