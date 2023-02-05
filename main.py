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




@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    message = str(message).split(":", 2)
    server = message[1].lstrip().rstrip()
    username=message[0].lstrip().rstrip()
    message=message[2].lstrip().rstrip()


    if message.startswith("https://youtu.be/") or message.startswith("https://www.youtube.com/watch?v="):
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
    if match.is_not_from_this_bot() and match.prefix():
        for i in commands:
            if match.command(i):
                response = commandprocessor(i)
                if response == None:
                    await bot.api.send_markdown_message(room.room_id, "странная ошибка, почините меня пжлста")
                else:
                    await bot.api.send_markdown_message(room.room_id, response)


def commandprocessor(command):
    if command == "ip":
        response = "На сервер можно зайти с версии 1.11.2 \nip адрес: advancedsoft.mooo.com"
    elif command == "map":
        response = "[Карта](http://advancedsoft.mooo.com:25552)"
    elif command == "fdi":
        response = "Микротест компонентов сервера в разработке"
        # 1 - проверить вебкарту ассинхронно, понять что основной серв работает
        # 2 - либой проверить что работает защитный прокси
    elif command == "help":
        response = "**!IP** - Дает ссылку на веб карту и инфу о сервере\n**!map** - Кинуть вебкарту\n**!fdi** - В разработке\n **!room** - Основная комната"
    else:
        response = "None"  #шта?
    return response

bot.run()
