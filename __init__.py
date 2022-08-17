from aiogram import executor, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.storage import FSMContext

from src.config import create_dirs, dp, load_json
from src.database import Database
from src.user import AdminState, User, UserState


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    user = User(message.from_user.id)
    await user.command_start()


@dp.message_handler(commands=['info'])
async def command_info(message: types.Message):
    user = User(message.from_user.id)
    await user.command_info(message)


@dp.message_handler(commands=['words'])
async def command_words(message: types.Message):
    user = User(message.from_user.id)
    await user.command_words(message)


@dp.message_handler(commands=['id'])
async def command_id(message: types.Message):
    user = User(message.from_user.id)
    await user.command_id()


@dp.message_handler(commands=['answer'])
async def command_answer(message: types.Message):
    user = User(message.from_user.id)
    await user.admin.command_answer()


@dp.message_handler(state=UserState.write_answer)
async def state_user_write(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    await user.write_answer(message, state)


@dp.message_handler(state=UserState.talk_answer)
async def state_user_talk(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    await user.talk_answer(message, state)


@dp.message_handler(state=AdminState.task_answer)
async def state_admin_answer(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    await user.admin.answer(message.text, state)


@dp.callback_query_handler(lambda call: call.data == 'menu_main_talk')
async def button_talk_task_start(call: types.CallbackQuery):
    user = User(call.from_user.id)
    await user.talk_task_start(call.message.message_id)


@dp.callback_query_handler(lambda call: call.data == 'menu_main_write')
async def button_write_task_start(call: types.CallbackQuery):
    user = User(call.from_user.id)
    await user.write_task_start(call.message.message_id)


@dp.callback_query_handler(lambda call: call.data == 'menu_main_listen')
async def button_listen_task_start(call: types.CallbackQuery):
    user = User(call.from_user.id)
    await user.listen_task_start(call.message.message_id)


@dp.callback_query_handler(lambda call: call.data == 'menu_main_read')
async def button_read_task_start(call: types.CallbackQuery):
    user = User(call.from_user.id)
    await user.read_task_start(call.message.message_id)


@dp.callback_query_handler(lambda call: call.data.startswith('talk'))
async def button_talk_task(call: types.CallbackQuery):
    user = User(call.from_user.id)
    await user.talk_task(call)


@dp.callback_query_handler(lambda call: call.data.startswith('write'))
async def button_write_task(call: types.CallbackQuery):
    user = User(call.from_user.id)
    await user.write_task(call)


@dp.callback_query_handler(lambda call: call.data.startswith('listen'))
async def button_listen_task(call: types.CallbackQuery):
    user = User(call.from_user.id)
    await user.listen_task(call)


@dp.callback_query_handler(lambda call: call.data.startswith('read'))
async def button_read_task(call: types.CallbackQuery):
    user = User(call.from_user.id)
    await user.read_task(call)


@dp.callback_query_handler(lambda call: call.data.startswith('words'))
async def button_words_page(call: types.CallbackQuery):
    user = User(call.from_user.id)
    await user.words(call)


async def startup(dp: Dispatcher):
    # create directories
    create_dirs()

    # load json files
    load_json()

    # create database
    await Database.create()

    # set commands
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Меню'),
        types.BotCommand('words', 'Необходимые слова'),
        types.BotCommand('info', 'Об экзамене')])

    # hidden commands: /id (Telegram id), /answer (check user answer and send reaction)


def main():
    # start bot polling
    executor.start_polling(
        dispatcher=dp,
        on_startup=startup)


if __name__ == '__main__':
    main()
