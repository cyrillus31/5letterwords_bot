import os

import telebot
from dotenv import load_dotenv

from src.util import is_valid_string, add_wildcards
from src.sql_main import Search

load_dotenv()

TOKEN = os.getenv("5LW_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="")

searches_dict = {}


@bot.message_handler(commands=["help", "start", "restart"])
def restart_search_or_help(message):
    new_search = Search()
    searches_dict[message.chat.id] = new_search
    bot.send_message(
        message.chat.id,
        """Этот бот помогает играть в игру 5букв
Отправь набор из пяти символов, который будет включать в себя известные тебе буквы Кириллицы и любые другие символы вместо неизвестных.
Затем, затем поставь запятую и напиши набор букв, которые точно есть в этом слове, а после - те, которых точно нет.
Например: _о$ка, кж, гязу
!!! Важно: обе запятые долджны стоят даже если вы хотит указать только нужные буквы или только ненужны!

Автор: @cyrillus31

Команды:
/restart - чтоыб сбросит все данные поиска
/status - чтобы посмотреть по каким параметрам ведется поиск""",
    )


@bot.message_handler(commands=["status"])
def status(message):
    try:
        new_search = searches_dict[message.chat.id]
        include, exclude = new_search.status()
        bot.send_message(
            message.chat.id,
            f"Буквы, которые должны быть: {include}\nБуквы, которых быть не должно: {exclude}",
        )
    except KeyError:
        searches_dict[message.chat.id] = Search()
        bot.send_message(message.chat.id, "Вы еще не указывали новые буквы")


@bot.message_handler()
def initial_message(message):
    if message.chat.id not in searches_dict:
        searches_dict[message.chat.id] = Search()
    new_search = searches_dict[message.chat.id]

    list_of_inputs = message.text.split(",")

    if len(list_of_inputs) == 3:
        myword, inc, exc = list_of_inputs
        new_search.append_include(inc)
        new_search.append_exclude(exc)
    else:
        myword = message.text

    if is_valid_string(myword):
        message_text = add_wildcards(myword)
        new_search.set_myword(message_text)
        reply_list = new_search.returns_list_of_words()
        if len(reply_list) > 100:
            reply = "Для данной комбинации букв подоходит более 100 различных слов. Попробуйте еще раз."
            bot.send_message(message.chat.id, reply)
        else:
            bot.send_message(message.chat.id, "\n".join(reply_list))
    else:
        bot.send_message(
            message.chat.id, "Неудачная комбинация букв! Попробуйте еще разок!"
        )


bot.infinity_polling()
