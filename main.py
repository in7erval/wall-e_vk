# -*- coding: utf-8 -*-
# Обратите внимание, версия лонгпула должна быть больше или равна 5.103
from vkwave.api import BotSyncSingleToken

TOKEN = '55cf82f4ab28d2f26bb5e86d0d9644207192dbfcdb39a45924c09e46d142a6f0aff00943648fd0c7719a2'
GROUP_ID = 178443094
# Импортируем нужные классы.
# SimpleLongPollBot: обёртка для более удобной работы с фреймворком
# SimpleBotEvent: тип события, который предоставляет SimpleLongPollBot
from vkwave.bots import SimpleLongPollBot, SimpleBotEvent, DocUploader
from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards.keyboard import ButtonColor
from constants import commands
from db import connection
import db
import generate
from vkwave.api import Token, BotSyncSingleToken, API
from vkwave.client import AIOHTTPClient
import os
import time

# инициализируем бота (можно ввести список токенов, тогда vkwave сможет обходить лимиты ВКонтакте)
bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)
client = AIOHTTPClient()
api = API(clients=client, tokens=BotSyncSingleToken(Token(TOKEN)),)
db.execute_query(connection,
                 """
CREATE TABLE IF NOT EXISTS messages( 
id INTEGER PRIMARY KEY AUTOINCREMENT,
peer_id INTEGER,
text TEXT NOT NULL,
from_id INTEGER);
""")


# help page
@bot.message_handler(bot.command_filter(commands=['help']))
async def command_help(event: SimpleBotEvent) -> str:
    help_text = "Текущие команды доступны: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    await event.answer(message=help_text)


@bot.message_handler(bot.command_filter('get_messages'))
async def handle(event: SimpleBotEvent) -> str:
    peer_id = event.object.object.message.peer_id
    return generate.get_strings(peer_id).__str__()


@bot.message_handler(bot.command_filter('get_dict'))
async def handle(event: SimpleBotEvent):
    peer_id = event.object.object.message.peer_id
    namefile = generate.dict_to_file(generate.create_dict(peer_id))
    doc = await DocUploader(api.get_context()).get_attachment_from_path(peer_id, namefile, title="Dictionary.txt")
    await event.answer(attachment=doc)
    time.sleep(2)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), namefile)
    os.remove(path)



@bot.message_handler(bot.command_filter('generate'))
async def handle(event: SimpleBotEvent) -> str:
    peer_id = event.object.object.message.peer_id # обращаемся к апи
    return generate.generate(peer_id, 20)
    # await event.answer(message=f"Привет, {user_data.first_name}")  # отправляем сообщение

# декоратор для создания обработчиков.
# можно передавать свои фильтры, но в данном случае мы хотим принимать все сообщения
@bot.message_handler()
async def handle(event: SimpleBotEvent) -> str:
    db.write_row(event)
    peer_id = event.object.object.message.peer_id
    # user_data = (await event.api_ctx.messages.get_by_conversation_message_id(
    # peer_id=event.object.object.message.peer_id).response[0]  # обращаемся к апи
    return generate.generate(peer_id, 20)
    # await event.answer(message=f"Привет, {user_data.first_name}")  # отправляем сообщение


# декоратор для создания обработчиков.
# можно передавать свои фильтры, но в данном случае мы хотим принимать все сообщения
@bot.message_handler()
async def write(event: SimpleBotEvent) -> str:
    # мы можем сразу возвращать текст, т.к vkwave понимает, что если вы возвращаете строку, то вы хотите ответить на
    # сообщение этим текстом. пользователь может задать свои типы данных, которые он сможет возвращать из хендлеров (
    # а также написать нужную логику для их преобразования в нужные действия)
    return "лох"


# запускаем бота с игнорированием ошибок (не останавливаться даже при них)
bot.run_forever()

if __name__ == '__main__':
	app.debug = True
	app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
