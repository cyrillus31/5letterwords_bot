import os

import telebot
from dotenv import load_dotenv

from src.util import is_valid_string, add_wildcards
from src.sql_main import returns_list_of_words

load_dotenv()

TOKEN = os.getenv("5LW_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="")

@bot.message_handler(commands=["help", "start"])
def send_help(message):
    bot.send_message(message.chat.id, "Этот бот помогает играть в игру 5букв\nОтправь набор из пяти символов, который будет включать в себя известные тебе буквы Кириллицы и любые другие символы вместо неизвестных.\nНапример: _о$ка")

@bot.message_handler()
def initial_message(message):
    if is_valid_string(message.text):
        message_text = add_wildcards(message.text)
        reply_list = returns_list_of_words(message_text)
        if len(reply_list) > 100:
            reply = "Для данной комбинации букв подоходит более 100 различных слов. Попробуйте еще раз."
            msg = bot.send_message(message.chat.id, reply)
            bot.register_next_step_handler(msg, initial_message)
        else:
            msg = bot.send_message(message.chat.id, "\n".join(reply_list))
            # bot.register_next_step_handler(msg, known_letters)
    else:
        bot.send_message(message.chat.id, "Неудачная комбинация букв! Попробуйте еще разок!")
        bot.register_next_step_handler(msg, initial_message)

bot.infinity_polling()