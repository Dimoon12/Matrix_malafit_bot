from mcstatus import JavaServer
import requests
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

urls = ["https://google.com", "http://advancedsoft.mooo.com", "http://advancedsoft.mooo.com:25552"]
commands = ["ip", "map", "diag", "help", "room"]


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
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
    elif command == "diag":
        response = "Еще в разработке"
    elif command == "help":
        response = "**!IP** - Дает ссылку на веб карту и инфу о сервере\n**!map** - Кинуть вебкарту\n**!diag** - В разработке\n **!room** - Основная комната"
    else:
        response = "None"  #шта?
    return response


bot.run()
