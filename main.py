# -*- coding: utf-8 -*-
import random
from datetime import datetime
import pytz
from vkwave.bots import SimpleLongPollBot, SimpleBotEvent, DocUploader, VoiceUploader, DefaultRouter
from vkwave.api import Token, BotSyncSingleToken, API
from vkwave.client import AIOHTTPClient
import os
import time
from gtts import gTTS
import logging
from vkwave.types.objects import MessagesMessageAttachmentType, BaseBoolInt
from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards.keyboard import ButtonColor

from constants import commands, sberkot_stickers
from db import connection
import db
import generate
from properties import TOKEN, GROUP_ID

TALKING = False

bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)
client = AIOHTTPClient()
api = API(clients=client, tokens=BotSyncSingleToken(Token(TOKEN)), )
router = DefaultRouter()
logging.basicConfig(level=logging.INFO)
db.execute_query(connection,
                 """
CREATE TABLE IF NOT EXISTS messages( 
id INTEGER PRIMARY KEY AUTOINCREMENT,
peer_id INTEGER,
text TEXT NOT NULL,
from_id INTEGER,
name TEXT NOT NULL default unknown,
date TEXT NOT NULL default unknown);
""")


# help page
@bot.message_handler(bot.command_filter(commands=['help']))
async def command_help(event: SimpleBotEvent):
    help_text = "Текущие команды доступны: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    await event.answer(message=help_text)


@bot.message_handler(bot.command_filter(('get_messages', 'history')))
async def handle(event: SimpleBotEvent) -> str:
    peer_id = event.object.object.message.peer_id
    return db.get_messages(peer_id)


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
async def generate_random(event: SimpleBotEvent) -> str:
    peer_id = event.object.object.message.peer_id
    return generate.generate(peer_id, 20)


@bot.message_handler(bot.text_filter("бот рандом"))
async def generate_random(event: SimpleBotEvent) -> str:
    peer_id = event.object.object.message.peer_id
    return generate.generate(peer_id, 20)


@bot.message_handler(bot.command_filter('say_random'))
async def handle(event: SimpleBotEvent):
    peer_id = event.object.object.message.peer_id
    text = generate.generate(peer_id, 20)
    await send_voice_message(event, peer_id, text)


@bot.message_handler(bot.text_filter("бот рандом скажи"))
async def handle(event: SimpleBotEvent):
    peer_id = event.object.object.message.peer_id
    text = generate.generate(peer_id, 20)
    await send_voice_message(event, peer_id, text)


@bot.message_handler(bot.text_startswith_filter("бот скажи"))
async def say_smth(event: SimpleBotEvent):
    peer_id = event.object.object.message.peer_id
    text = event.object.object.message.text.split('бот скажи')
    if len(text[1]) != 0:
        await send_voice_message(event, peer_id, text[1])


@bot.message_handler(bot.text_startswith_filter(("насколько", "на сколько")))
async def probability(event: SimpleBotEvent) -> str:
    message_text = event.object.object.message.text
    if "насколько" in message_text.lower():
        res = message_text.lower().split("насколько", 2)
    elif "на сколько" in message_text.lower():
        res = message_text.lower().split("на сколько", 2)
    if len(res) > 1:
        prob = random.randint(0, 101)
        if " я " in res[1]:
            res[1] = res[1].replace(" я ", " ты ")
        elif " ты " in res[1]:
            res[1] = res[1].replace(" ты ", " я ")
        return "Я думаю, что" + res[1] + " на " + str(prob) + "%"


@bot.message_handler(bot.text_contains_filter("или"), bot.text_startswith_filter("бот"))
async def choice(event: SimpleBotEvent) -> str:
    message_text = event.object.object.message.text
    res = message_text.lower().split("бот ")[1].split(" или ")
    for x in res:
        if " я " in x:
            x = x.replace(" я ", " ты ")
        elif x.startswith("я"):
            x = x.replace("я", "ты", 1)
        elif " ты " in x:
            x = x.replace(" ты ", " я ")
        elif x.startswith("ты"):
            x = x.replace("ты", "я", 1)
    prefixes = ["Определённо", "Ну я думаю", "Наверное", "Ну тут по любому"]
    return random.choice(prefixes) + " " + random.choice(res)


@bot.message_handler(bot.text_filter(("бот пришли клавиатуру", "бот клавиатура", "бот кнопки")))
async def send_keyboard(event: SimpleBotEvent):
    kb = Keyboard(one_time=True)
    kb.add_text_button("бот рандом", color=ButtonColor.PRIMARY)
    kb.add_text_button("бот рандом скажи", color=ButtonColor.PRIMARY)
    await event.answer(message="На", keyboard=kb.get_keyboard())


@bot.message_handler(bot.text_contains_filter('сука'))
async def send_sticker(event: SimpleBotEvent):
    await event.answer(sticker_id=random.choice(sberkot_stickers))


@bot.message_handler(bot.command_filter('talking'))
async def talking(event: SimpleBotEvent) -> str:
    global TALKING
    TALKING = not TALKING
    if TALKING:
        return 'еее снова болтаю'
    else:
        return 'заткнулся'


@bot.message_handler(bot.text_filter(('бот завали ебало', 'бот заткнись')))
async def talking(event: SimpleBotEvent) -> str:
    global TALKING
    if not TALKING:
        ans = "и так молчу лол"
    else:
        ans = "лан молчу"
    TALKING = False
    return ans


@bot.message_handler()
async def handle(event: SimpleBotEvent) -> str:
    peer_id = event.object.object.message.peer_id
    message = event.object.object.message
    logging.info("Сообщение %s", message)
    if len(message.attachments) > 0:
        attachment = message.attachments[0]
        logging.info("Есть вложение типа %s", attachment.type)
        if attachment.type == MessagesMessageAttachmentType.STICKER:
            db.save_sticker(peer_id, attachment.sticker.sticker_id)
            resp = await event.answer(message='ща удалится')
            time.sleep(1)
            await (api.get_context()).messages.delete(message_ids=resp.response, delete_for_all=BaseBoolInt.YES)
        elif attachment.type == MessagesMessageAttachmentType.PHOTO:
            return "нахуй фотки шлешь пидорас"
        elif attachment.type == MessagesMessageAttachmentType.DOC:
            return "и че это за хуебина"
    else:
        await prepare_and_write(event)
        await event.answer(reply_to=message.id, message='message')
        if TALKING:
            return generate.generate(peer_id, 20)


async def prepare_and_write(event):
    user = (await api.get_context().users.get(user_ids=event.object.object.message.from_id)).response[0]
    name = user.first_name + ' ' + user.last_name
    date = datetime.fromtimestamp(event.object.object.message.date, tz=pytz.timezone('Europe/Moscow')).strftime(
        "%Y-%m-%d %H:%M:%S")
    db.write_row(event, name, date)


async def send_voice_message(event, peer_id, text):
    tts = gTTS(text, lang='ru')
    filename = "audio_" + datetime.now().strftime("%y%m%d_%H%M%S") + ".ogg"
    tts.save(filename)
    doc = await VoiceUploader(api.get_context()).get_attachment_from_path(peer_id, filename, title="audio.ogg")
    await event.answer(attachment=doc)
    time.sleep(2)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    os.remove(path)


bot.run_forever()
