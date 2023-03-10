# from mcstatus import JavaServer
import requests
import asyncio
import random
import os
from pytube import YouTube
import simplematrixbotlib as botlib

# не трогать
config = botlib.Config()
config.encryption_enabled = True
config.emoji_verify = True
config.ignore_unverified_devices = True

with open("cred.txt", "r") as f:
    login, password = f.read().split(":")
creds = botlib.Creds("https://cuteworld.space", f"{login}", f"{password}")

with open("admins.txt", "r") as f:
    adminnicks = f.read()
with open("moders.txt", "r") as f:
    modersnicks = f.read()

bot = botlib.Bot(creds, config)

# Long Settings
PREFIX = '!'
commands = ["ip", "map", "help", "learnsw", "aisw"]
phrasesworkingonit = ["Ненавижу свою ебаную работу, ща погоди", "Ща сделаю, сек", "Ааа бля ща ща сделаю",
                      "Делаю уже, погоди", "Погоди, ща все сделаем, только поем оперативки"]
phraseshardworkdone = ["На, наслаждайся", "Вот, не подавись", "На, вот", "Сделал", "Тадаам"]
# Stable settings
youtubedownload = True
statelearn = True
# Beta and alpha settings
beta_recognitionhttp = True

# Http server for recognition parameters
httpfbport = "5000"
httpfbhost = "localhost"


# Отправка админам об ошибках
async def sendfault(fault):
    await bot.api.send_markdown_message("!rIdzntOJyjfoCpBCYS:cuteworld.space", fault)


@bot.listener.on_message_event
async def echo(room, message):
    global commandexecuted
    commandexecuted = False
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    message = str(message).split(":", 2)
    server = message[1].strip()
    username = message[0].strip()
    message = message[2].strip()

    ## загрузка всякой херни по ссылке
    if message.startswith("https://youtu.be/") or message.startswith(
            "https://www.youtube.com/watch?v=") or message.startswith(
        "https://youtube.com/") and youtubedownload == True:
        commandexecuted = True
        try:
            os.remove("download.mp4")
        except:
            pass
        # choose random phrase from list and send it
        response = random.choice(phrasesworkingonit)
        await bot.api.send_markdown_message(room.room_id, response)
        video = YouTube(f'{message}')
        try:
            if video.length > 3600:
                await bot.api.send_markdown_message(room.room_id, f"Видео больше часа, пошел ты нахуй")
                return
            video.streams.filter(res="360p").first().download(filename="download.mp4")
            await bot.api.send_video_message(room.room_id, "download.mp4")
            os.remove("download.mp4")
            await bot.api.send_markdown_message(room.room_id, f"Название: **{video.title}**")
        except:
            await bot.api.send_markdown_message(room.room_id,
                                                f"Я не могу скачать видео. У тебя дерьмовая ссылка <a href='https://matrix.to/#/{username}:{server}'>{username}</a> !")
            loop = asyncio.get_running_loop()
            loop.create_task(sendfault("**[ERR] [YouTube]** Не смог скачать по ссылке, битая или видео недоступно без акка и тп"))

    ## команды
    if match.is_not_from_this_bot() and match.prefix():
        commandexecuted = True
        for i in commands:
            if match.command(i):
                response = commandprocessor(i, username)
                if response == None:
                    pass
                else:
                    await bot.api.send_markdown_message(room.room_id, response)

    # beta_fallback
    message = message.lower()
    if beta_recognitionhttp and match.is_not_from_this_bot() and not commandexecuted:
        response = fallback_actions(message)
        if not response == None:
            await bot.api.send_markdown_message(room.room_id, response)


def commandprocessor(command, username):
    global statelearn
    global response
    global beta_recognitionhttp
    if command == "aisw":
        if checkpermissions(username, 2):
            if beta_recognitionhttp == True:
                beta_recognitionhttp = False
                response = "Чат режим выключен"
                loop = asyncio.get_running_loop()
                loop.create_task(sendfault(
                    f"*[Caution] [Параметры]* Чат режим глобально выключен {username}"))
            else:
                beta_recognitionhttp = True
                response = "Чат режим включен"
                loop = asyncio.get_running_loop()
                loop.create_task(sendfault(
                    f"*[Caution] [Параметры]* Чат режим глобально выключен {username}"))
        else:
            response = "Недостаточный уровень привелегий"
            print(response)

    elif command == "learnsw":
        if checkpermissions(username, 2):
            if statelearn:
                statelearn = False
                response = "Обучение выключено"
                loop = asyncio.get_running_loop()
                loop.create_task(sendfault(
                    f"*[Caution] [Параметры]* Обучение глобально выключено {username}"))
            else:
                statelearn = True
                response = "Обучение включено"
                loop = asyncio.get_running_loop()
                loop.create_task(sendfault(
                    f"*[Caution] [Параметры]* Обучение глобально включено {username}"))
        else:
            response = "Недостаточный уровень привелегий"
    elif command == "ip":
        response = "На сервер можно зайти с версии 1.11.2 \nip адрес: advancedsoft.mooo.com"
    elif command == "map":
        response = "[Карта](http://advancedsoft.mooo.com:25552)"
    elif command == "help":
        response = "**!IP** - Дает ссылку на веб карту и инфу о сервере\n**!map** - Кинуть вебкарту\n**!fdi** - В разработке\n**!aisw** - Переключить диалоговый режим бота \n**!learnsw** - Переключить режим обучения"
    else:
        response = None
        loop = asyncio.get_running_loop()
        loop.create_task(
            sendfault("**[ERR] [Команда]** Ошибка при исполнении команды, команда есть в списке но нет вывода"))
    return response


def checkpermissions(user, required):
    access = 1
    if user in modersnicks:
        access = 2
    if user in adminnicks:
        access = 3
    if access < required:
        return False
    else:
        return True


def preparemessage(message):
    splited = []
    answer="no_reply"
    question=message
    splited = message.split(">")
    if len(splited) > 1:
        splited = splited[2].split("\n\n")
        question = splited[0].lower().strip()
        answer = splited[1].lower().strip()
        loop = asyncio.get_running_loop()
        loop.create_task(sendfault(
            f"*[DBG] [http обучение]* Ответ: {answer} Вопрос: {question}  Разрешение: {statelearn}"))

    response=requests.get(f'http://{httpfbhost}:{httpfbport}/get_answer',
                 params={'text': question, 'reply_text': answer, 'space': 'matrix'})
    response=response.text.lower().strip()
    if "err" in response or "wrn" in response:
        loop = asyncio.get_running_loop()
        loop.create_task(sendfault(
            f"**[ERR/WRN][Адаптер http]** {response}"))
        response=None
    return(response)


def fallback_actions(message):
     return(preparemessage(message))



bot.run()