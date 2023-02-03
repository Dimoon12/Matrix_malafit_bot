
from mcstatus import JavaServer
import requests
import simplematrixbotlib as botlib

config = botlib.Config()
config.encryption_enabled = True
config.emoji_verify = True
config.ignore_unverified_devices = True


#get credentials from file cred.txt, splitted with :
with open("cred.txt", "r") as f:
    login, password = f.read().split(":")


creds = botlib.Creds("https://matrix.org", f"{login}", f"{password}")

bot = botlib.Bot(creds, config)
PREFIX = '!'
urls=["https://google.com","http://advancedsoft.mooo.com","http://advancedsoft.mooo.com:25552"]



@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("diag"):
        await bot.api.send_text_message(room.room_id,"Выполняю тесты, пожалуйста подождите, бот может подвиснуть\n(Первый хост для проверки инета, второй для проверки работы железа, третий для проверки freedomcraft основного сервера, защитный прокси freedomcraft проверяется в конце)")
        for i in urls:
            try:
                r = requests.get(i, timeout=2)
                response = r.status_code
            except:
                response = "Возможно таймаут"
            finally:
                if not response == 200:
                    await bot.api.send_text_message(room.room_id, f"{i} - НЕДОСТУПЕН Ответ: {response}")
                else:
                    await bot.api.send_text_message(room.room_id, f"{i} - доступен")
        try:
            server = JavaServer.lookup("advancedsoft.mooo.com:25565")
            serverdata= server.status()
            await bot.api.send_text_message(room.room_id, f"Freedomcraft - защитный прокси {serverdata.players.online} игроков, пинг {serverdata.latency}")
        except:
            await bot.api.send_markdown_message(room.room_id, f"Freedomcraft- защитный прокси НЕДОСТУПЕН")
        await bot.api.send_text_message(room.room_id, "Диагностика завершена!")



    elif match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("test"):
        await bot.api.send_text_message(room.room_id,"Иди нахуй")

    elif match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("ip"):
        await bot.api.send_text_message(room.room_id,"На сервер можно зайти с версии 1.11.2 \nip адрес: advancedsoft.mooo.com")

    elif match.is_not_from_this_bot() \
          and match.prefix() \
          and match.command("help"):
             await bot.api.send_markdown_message(room.room_id, "БЕТА ТЕСТ ЕБАЦ, бот пока что не на постоянке, и фич мега мало, ждите\n**!IP** - Дает ссылку на веб карту и инфу о сервере\n**!test** - Посылает нахуй\n**!map** - Кинуть вебкарту\n**!diag** - Временная реализация общей диагностики\n **!room** - Основная комната")

    elif match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("map"):
        await bot.api.send_markdown_message(room.room_id,"[Карта](http://advancedsoft.mooo.com:25552)")

    elif match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("room"):
        await bot.api.send_markdown_message(room.room_id,"[Комната](https://matrix.to/#/!bcoWUUOVMNaVwTvSda:anontier.nl?via=anontier.nl)")

bot.run()