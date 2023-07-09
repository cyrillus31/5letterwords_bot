"""
https://t.me/FiveLetterWordsBot
author: @IdoubledareU31
        kirill.olegovich31@gmail.com

Привет! Этот бот поможет подобрать слово (существительное) из ПЯТИ букв русского алфавита на основании известных и неизвестных букв.

"""


import telebot
import re

with open("token.txt", "r") as f:
    token = f.read()

bot = telebot.TeleBot(token)

theword = ""
theletters = ""
letters_list = []
unfitletters = ""
unfitletters_list = []
url = ""
this_chat_id = ""


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Этот бот поможет тебе подобрать слово из ПЯТИ букв русского алфавита на основании известных букв.\n\n"
        "Шаг 1 из 3: \nВведите слово заменяя неизвестные буквы знаком '+' Например: л++ка",
    )


@bot.message_handler(commands=["clean"])
def clean(message):
    try:
        with open("theletters{}.txt".format(message.chat.id), "r") as f:
            x = f.readline()
            print(x + " look here")

        with open("unfitletters{}.txt".format(message.chat.id), "r") as f:
            y = f.readline()
            print(y + " look here")

        if len(x) == 0 and len(y) == 0:
            bot.send_message(message.chat.id, "Чистка не требуется!")
        else:
            with open("theletters{}.txt".format(message.chat.id), "w") as f:
                f.write("")
            with open("unfitletters{}.txt".format(message.chat.id), "w") as f:
                f.write("")
            bot.send_message(
                message.chat.id,
                "Хранилась информация о следующийх буквах: {} {}\n Архив почищен!".format(
                    x, y
                ),
            )

    except Exception as err:
        bot.send_message(message.chat.id, "Чистка не требуется!!!")


@bot.message_handler(func=lambda x: True)
def enter_the_word(message):
    global theword
    theword = message.text.lower()
    msg = bot.send_message(
        message.chat.id,
        "Шаг 2 из 3: \nСлово принято! Теперь, пожалуйста, введите подряд буквы, которых точно НЕТ в слове. Либо отправьте цифру ноль.",
    )
    bot.register_next_step_handler(msg, enter_unfit_letters)


def enter_unfit_letters(message):
    global unfitletters, unfitletters_list
    if message.text == "0":
        bot.send_message(message.chat.id, "Значит таких букв нет? ОК!")
        unfitletters = ""
    else:
        bot.send_message(message.chat.id, "Буквы приняты!")
        unfitletters = message.text.lower()

    # add unfit letters to the existing file theletters.txt and generrate updated letters_list
    with open("unfitletters{}.txt".format(message.chat.id), "a") as f:
        f.write(unfitletters)
    with open("unfitletters{}.txt".format(message.chat.id), "r") as file:
        x = file.readline()
        print(x)

    unfitletters_list = [letter for letter in x]
    unfitletters = ("").join(unfitletters_list)
    print(unfitletters_list)

    msg = bot.send_message(
        message.chat.id,
        "Шаг 3 из 3: \nСлово принято! Теперь, пожалуйста, введите подряд буквы, которые присутствуют в слове, но позиция которых неизвестна. Например: ож  Если таких букв нет или не появились новые, то отправь цифру ноль.",
    )
    bot.register_next_step_handler(msg, enter_the_letters)


def enter_the_letters(message):
    global theletters, letters_list, url, theword, unfitletters, unfitletters_list
    if message.text == "0":
        bot.send_message(
            message.chat.id,
            "Значит таких букв нет? Хорошо, начинаем искать подходящие слова!",
        )
        theletters = ""
    else:
        bot.send_message(
            message.chat.id, "Буквы приняты! Начинаем искать подходящие слова!"
        )
        theletters = message.text.lower()

    # add the letters to the existing file theletters.txt and generate updated letters_list
    with open("theletters{}.txt".format(message.chat.id), "a") as f:
        f.write(theletters)
    with open("theletters{}.txt".format(message.chat.id), "r") as file:
        x = file.readline()
        print(x)

    letters_list = [letter for letter in x]
    theletters = ("").join(letters_list)
    print(theletters + " fit letters")

    try:
        with open("all5letterwords.txt", "r") as f:
            allwords_string = f.read()
            # allwords_list = f.read().split(", ")
        print(theword)

        pattern = r""
        for letter in theword:
            if letter == "+":
                pattern += "[а-я]"
            else:
                pattern += letter
        print(pattern)

        thewords_list = re.findall(pattern, allwords_string)
        # print(thewords_list)

        finalwords_list = []

        # filter the words in thewords_list using letters_list AND unfitletters_list
        for word in thewords_list:
            result = True
            for letter in letters_list:
                result *= letter.lower() in word
            if bool(result):
                finalwords_list.append(word)
        print(finalwords_list)

        finalwords_list_extra = finalwords_list[:]
        if len(unfitletters_list) != 0:
            for word in finalwords_list_extra:
                for letter in unfitletters_list:
                    if letter.lower() in word:
                        finalwords_list.remove(word)
                        print(finalwords_list)
                        break
        # # print(thewords_list)

        answer = ", ".join(finalwords_list)
        # print(answer+"  вот ответ")
        if len(answer) == 0:
            bot.send_message(
                message.chat.id, "Похоже, что таких слов нет! Попробуйте заново"
            )
            open("theletters{}.txt".format(message.chat.id), "w").close()
            open("unfitletters{}.txt".format(message.chat.id), "w").close()
            msg = bot.send_message(
                message.chat.id,
                "Шаг 1 из 3: \nВведите это же слово заменяя неизвестные буквы знаком '+' Например: в+л+а",
            )
            bot.register_next_step_handler(msg, enter_the_word)
        else:
            bot.send_message(message.chat.id, answer)
            msg = bot.send_message(
                message.chat.id, "Хотите внести уточнения в этот поиск? да/нет"
            )
            bot.register_next_step_handler(msg, return_the_loop)

    except Exception as err:
        print("Ууууупс!")
        print(err)
        bot.send_message(
            message.chat.id, "Ууууупс! Что-то пошло не так.\n\n Попробуйте заново!"
        )
        bot.send_message(
            message.chat.id,
            "Шаг 1 из 3: \nВведите слово заменяя неизвестные буквы знаком '+' Например: в+л+а",
        )

        # clean the file with letters
        open("theletters{}.txt".format(message.chat.id), "w").close()
        open("unfitletters{}.txt".format(message.chat.id), "w").close()


def return_the_loop(message):
    global shall_continue
    if message.text.lower()[0] == "д":
        bot.send_message(
            message.chat.id,
            "Шаг 1 из 3: \nВведите это же слово заменяя неизвестные буквы знаком '+' Например: в+л+а",
        )
        print("shall continue")
        # update file with letters

    elif message.text.lower()[0] == "н":
        print("shall stop")
        # clean the file with letters
        open("theletters{}.txt".format(message.chat.id), "w").close()
        open("unfitletters{}.txt".format(message.chat.id), "w").close()
        bot.send_message(message.chat.id, "Архив почищен!")
        bot.send_message(
            message.chat.id,
            "Шаг 1 из 3: \nВведите слово заменяя неизвестные буквы знаком '+' Например: в+л+а",
        )


bot.polling()
