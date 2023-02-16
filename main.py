from mcstatus import JavaServer
import requests
import asyncio
import random
import re
import os
from pytube import YouTube
import simplematrixbotlib as botlib

##не трогать
config = botlib.Config()
config.encryption_enabled = True
config.emoji_verify = False
config.ignore_unverified_devices = True

with open("cred.txt", "r") as f:
    login, password = f.read().split(":")
creds = botlib.Creds("https://matrix.org", f"{login}", f"{password}")

bot = botlib.Bot(creds, config)
PREFIX = '!'
commands = ["ip", "map", "help", "room", "chat"]
phrasesworkingonit = ["Ненавижу свою ебаную работу, ща погоди", "Ща сделаю, сек", "Ааа бля ща ща сделаю", "Делаю уже, погоди", "Погоди, ща все сделаем, только поем оперативки"]
phraseshardworkdone = ["На, наслаждайся", "Вот, не подавись", "На, вот", "Сделал", "Тадаам"]

# Stable settings
youtubedownload=True
# Beta and alpha settings
beta_recognitionhttp=True
alpha_enablefallbackwarning=False
#Additional settings
httpfbport="5000"
httpfbhost="localhost"



#Отправка админам об ошибках
async def sendfault(fault):
    await bot.api.send_text_message("!GhhKvYgrxKgvoPoSgq:anontier.nl", fault)

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    message = str(message).split(":", 2)
    server = message[1].strip()
    username=message[0].strip()
    message=message[2].strip()

## загрузка всякой херни по ссылке
    if message.startswith("https://youtu.be/") or message.startswith("https://www.youtube.com/watch?v=") or message.startswith("https://youtube.com/") and youtubedownload==True:
        try:
            os.remove("download.mp4")
        except:
            pass
        #choose random phrase from list and send it
        response=random.choice(phrasesworkingonit)
        await bot.api.send_markdown_message(room.room_id, response)
        try:
            video = YouTube(f'{message}')
            if video.length > 3600:
                await bot.api.send_markdown_message(room.room_id, f"Видео больше часа, пошел ты нахуй")
                return
            video.streams.filter(res="360p").first().download(filename="download.mp4")
            await bot.api.send_video_message(room.room_id, "download.mp4")
            os.remove("download.mp4")
            await bot.api.send_markdown_message(room.room_id, f"Название: **{video.title}**")
        except:
            await bot.api.send_markdown_message(room.room_id, f"Я не могу скачать видео. У тебя дерьмовая ссылка <a href='https://matrix.to/#/{username}:{server}'>{username}</a> !")
            loop = asyncio.get_running_loop()
            loop.create_task(sendfault("[YouTube] Не смог скачать по ссылке, битая или недоступна и тп"))



#beta_fallback
    if beta_recognitionhttp and match.is_not_from_this_bot():
       response = fallback_actions(message)
       if not response == None:
           if alpha_enablefallbackwarning:
               await bot.api.send_markdown_message(room.room_id, f"(RECOGNITION) {response}")
           else:
               await bot.api.send_markdown_message(room.room_id, response)
       else:
           loop = asyncio.get_running_loop()
           loop.create_task(sendfault("[Адаптер http] Получил пустое сообщение, игнорирую"))


## команды
    if match.is_not_from_this_bot() and match.prefix():
        for i in commands:
            if match.command(i):
                response = commandprocessor(i)
                if response == None:
                    pass
                else:
                    await bot.api.send_markdown_message(room.room_id, response)



def commandprocessor(command):
    #if command == "chat":
       # if beta_recognitionhttp == True:
       #     response = "Модуль выключен"
       #     beta_recognitionhttp = False
       # else:
       #     response = "Модуль включен! (БЕТА)"
       #     beta_recognitionhttp = True
    if command == "ip":
        response = "На сервер можно зайти с версии 1.11.2 \nip адрес: advancedsoft.mooo.com"
    elif command == "map":
        response = "[Карта](http://advancedsoft.mooo.com:25552)"
    elif command == "help":
        response = "**!IP** - Дает ссылку на веб карту и инфу о сервере\n**!map** - Кинуть вебкарту\n**!fdi** - В разработке\n **!room** - Основная комната"
    else:
        response='None'
        loop = asyncio.get_running_loop()
        loop.create_task(sendfault("[Команда] Ошибка при исполнении команды, команда есть в списке но нет вывода"))
    return response



def fallback_actions(message):
    if not beta_recognitionhttp:
       pass
    else:
        print("Fallback http Executed (debug)")
        response=requests.get(f'http://{httpfbhost}:{httpfbport}/get_answer', params={'text': message, 'reply_text': 'no_reply'})
        try:
           response2=response.text
        except:
            response2 = "None"
            loop = asyncio.get_running_loop()
            loop.create_task(sendfault(f"[Адаптер http] Получены данные из которых нельзя получить текст json: {response.json} statuscode: {response.status_code} "))
        if "err" in response2:
            loop = asyncio.get_running_loop()
            loop.create_task(sendfault(
                f"[Адаптер http] Ошибка сервера {response2}"))
            response2 = None
        return(response2)
bot.run()
