from mcstatus import JavaServer
import requests
import asyncio
import random
import re
import os
from pytube import YouTube
import simplematrixbotlib as botlib

## шифровальное говно, не трогать
config = botlib.Config()
config.encryption_enabled = True
config.emoji_verify = False
config.ignore_unverified_devices = True

with open("cred.txt", "r") as f:
    login, password = f.read().split(":")
creds = botlib.Creds("https://matrix.org", f"{login}", f"{password}")

bot = botlib.Bot(creds, config)
PREFIX = '!'
commands = ["ip", "map", "fdi", "help", "room"]
phrasesworkingonit = ["Ненавижу свою ебаную работу, ща погоди", "Ща сделаю, сек", "Ааа бля ща ща сделаю", "Делаю уже, погоди", "Погоди, ща все сделаем, только поем оперативки"]
phraseshardworkdone = ["На, наслаждайся", "Вот, не подавись", "На, вот", "Сделал", "Тадаам"]

# Stable settings
youtubedownload=True
# Beta and alpha settings
beta_mp4download=False
beta_fallbackhttp=False
#Additional
httpfbport="1111"
httpfbhost="localhost"


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

    #Временно, надо на async
    if message.endswith(".mp4") and message.startswith("https") and beta_mp4download==True:
        try:
            print("Beta download mp4")
            data=requests.get(message)
            open('download.mp4', 'wb').write(data.content)
            data=0
            await bot.api.send_video_message(room.room_id, "download.mp4")
        except:
            await bot.api.send_markdown_message(room.room_id, f"Ошибка скачивания (betamode)")


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
    if command == "ip":
        response = "На сервер можно зайти с версии 1.11.2 \nip адрес: advancedsoft.mooo.com"
    elif command == "map":
        response = "[Карта](http://advancedsoft.mooo.com:25552)"
    elif command == "fdi" and beta_checkfreedomnetwork==True:
        response = "Микротест компонентов сервера в разработке"
        # 1 - проверить вебкарту ассинхронно, понять что основной серв работает
        # 2 - либой проверить что работает защитный прокси
    elif command == "help":
        response = "**!IP** - Дает ссылку на веб карту и инфу о сервере\n**!map** - Кинуть вебкарту\n**!fdi** - В разработке\n **!room** - Основная комната"
    else:
        fallback_actions()
        response = "None"
    return response

def fallback_actions():
    if not beta_fallbackhttp:
       await bot.api.send_markdown_message(room.room_id, "странная ошибка, почините меня пжлста")
       print("Unknown error (debug)")
    else:
        requests.get(f'{httpfbhost}:{httpfbport}/{message}')
        print("FallbackhttpExecuted (debug)")

bot.run()
