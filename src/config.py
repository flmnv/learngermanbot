import json
import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

BOT_TOKEN = ''

ANSWERS = {}
ADMIN_ANSWERS = {}
FILES: json

bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


def load_json():
    global LEARN, FILES

    with open('data/json/learn.json', 'r', encoding='utf-8') as learn_file:
        LEARN = json.load(learn_file)

    if not os.path.exists('data/json/id.json'):
        with open(f'data/json/id.json', 'w', encoding='utf-8') as id_file:
            json.dump(obj={}, fp=id_file, ensure_ascii=False, indent=4)

    with open('data/json/id.json', 'r', encoding='utf-8') as id_file:
        FILES = json.load(id_file)


def create_dirs():
    if not os.path.exists('db'):
        os.mkdir('db')

    if not os.path.exists('data/img'):
        os.mkdir('data/img')

    if not os.path.exists('data/vid'):
        os.mkdir('data/vid')
