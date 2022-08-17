from random import randint, shuffle

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.inline_keyboard import (InlineKeyboardButton,
                                           InlineKeyboardMarkup)

import src.config as config
from src.config import bot
from src.database import Database
from src.tgfiles import TGFile


class Learn:
    """
    Base learn class
    """

    def __init__(self) -> None:
        self.menu = LearnMenu()

    async def exam_info(self, chat_id: int, message_id: int = None):
        """
        Use this method to send or edit a message to the exam info

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`

        :return: On success, returns a sent or edited message
        :rtype: :obj:`types.Message`
        """
        if message_id:
            return await bot.edit_message_text(
                config.LEARN['ExamInfo'],
                chat_id, message_id,)

        return await bot.send_message(
            chat_id, config.LEARN['ExamInfo'])

    async def words(self, chat_id: int, page: int = 0, message_id: int = None, count: int = 10):
        """
        Use this method to send or edit a message to the words page

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param page: Page number
        :type page: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`
        :param count: Maximum number of words per page
        :type count: :obj:`int`

        :return: On success, returns a sent or edited message
        :rtype: :obj:`types.Message`
        """
        if page * count > len(config.LEARN['Words']):
            return

        inline_keyboard = InlineKeyboardMarkup()
        fst_word = page * count
        until_word = min((page + 1) * count, len(config.LEARN['Words']))
        buttons = []

        page_words = config.LEARN['Words'][fst_word:until_word]
        msg_text = f'<b>Страница {page + 1}</b>\n'

        for word in page_words:
            msg_text += f'\n{word}'

        if fst_word != 0:
            buttons.append(
                InlineKeyboardButton(
                    text='« Назад',
                    callback_data=f'words_{page - 1}'))

        if until_word < len(config.LEARN['Words']):
            buttons.append(
                InlineKeyboardButton(
                    text='Далее »',
                    callback_data=f'words_{page + 1}'))

        inline_keyboard.add(*buttons)

        if message_id:
            return await bot.edit_message_text(
                msg_text, chat_id, message_id,
                parse_mode='html',
                reply_markup=inline_keyboard)

        return await bot.send_message(
            chat_id, msg_text,
            parse_mode='html',
            reply_markup=inline_keyboard)


class LearnMenu:
    """
    Base menu class
    """

    def __init__(self) -> None:
        self.__button_talk = InlineKeyboardButton(
            text='Sprechen',
            callback_data='menu_main_talk')

        self.__button_write = InlineKeyboardButton(
            text='Schreiben',
            callback_data='menu_main_write')

        self.__button_listen = InlineKeyboardButton(
            text='Hören',
            callback_data='menu_main_listen')

        self.__button_read = InlineKeyboardButton(
            text='Lesen',
            callback_data='menu_main_read')

    async def send(self, chat_id: int):
        """
        Use this method to send the learn menu

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`

        :return: On success, returns a sent message
        :rtype: :obj:`types.Message`
        """
        inline_keyboard = InlineKeyboardMarkup(row_width=2)

        inline_keyboard.add(
            self.__button_talk,
            self.__button_write,
            self.__button_listen,
            self.__button_read)

        return await bot.send_message(
            chat_id=chat_id,
            text='Подготовка к экзамену по немецкому (часть А1)',
            reply_markup=inline_keyboard)

    async def __get_random_except(self, max_num: int, except_num: int):
        """
        Use this method to get a random value, except for one value

        :param max_num: Maximum value
        :type max_num: :obj:`int`
        :param except_num: Except value
        :type except_num: :obj:`int`

        :return: Returns a random value, except for one value
        :rtype: :obj:`int`
        """
        rand = randint(0, max_num)

        while rand == except_num:
            rand = randint(0, max_num)

        return rand

    async def read_task(self, chat_id: int, message_id: int = None, task: int = None):
        """
        Use this method to send or edit a message to a new read task

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`
        :param task: Last task number
        :type task: :obj:`int`

        :return: On success, returns a sent or edited message
        :rtype: :obj:`types.Message`
        """
        inline_keyboard = InlineKeyboardMarkup()
        new_task: int

        if task is not None:
            new_task = await self.__get_random_except(
                len(config.LEARN['Read']) - 1, task)
        else:
            new_task = randint(0, len(config.LEARN['Read']) - 1)

        task_text = config.LEARN['Read'][new_task]['text']
        task_answers = [
            InlineKeyboardButton(
                text=config.LEARN['Read'][new_task]['answers'][0],
                callback_data=f'read_{new_task}_correct')]

        if 'row_width' in config.LEARN['Read'][new_task]:
            inline_keyboard.row_width = config.LEARN['Read'][new_task]['row_width']

        for a_num in range(1, len(config.LEARN['Read'][new_task]['answers'])):
            task_answers.append(
                InlineKeyboardButton(
                    text=config.LEARN['Read'][new_task]['answers'][a_num],
                    callback_data=f'read_{new_task}_wrong'))

        shuffle(task_answers)
        inline_keyboard.add(*task_answers)

        if message_id:
            return await bot.edit_message_text(
                task_text, chat_id, message_id,
                reply_markup=inline_keyboard)

        return await bot.send_message(
            chat_id, task_text,
            reply_markup=inline_keyboard)

    async def read_result(self, chat_id: int, task: int,
                          answer: bool, message_id: int = None):
        """
        Use this method to send or edit a message on the result of the task

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param task: Last task number
        :type task: :obj:`int`
        :param answer: Correct or wrong
        :type answer: :obj:`bool`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`

        :return: On success, returns a sent or edited message
        :rtype: :obj:`types.Message`
        """
        inline_keyboard = InlineKeyboardMarkup()
        result_text: str

        if answer:
            result_text = f'Правильно! 🥳'
        else:
            result_text = f'Неправильно. 😔 \nПравильный ответ был: <b>«{config.LEARN["Read"][task]["answers"][0]}»</b>.'

        inline_keyboard.add(
            InlineKeyboardButton(
                text='Продолжить »',
                callback_data=f'read_{task}'))

        if message_id:
            return await bot.edit_message_text(
                result_text, chat_id, message_id,
                parse_mode='html',
                reply_markup=inline_keyboard)

        return await bot.send_message(
            chat_id, result_text,
            parse_mode='html',
            reply_markup=inline_keyboard)

    async def listen_task(self, chat_id: int, message_id, task: int = None):
        """
        Use this method to send a new listen task message

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`
        :param task: Last task number
        :type task: :obj:`int`

        :return: On success, returns a message
        :rtype: :obj:`types.Message`
        """
        inline_keyboard = InlineKeyboardMarkup()
        new_task: int

        await bot.edit_message_reply_markup(
            chat_id, message_id)

        if task is not None:
            new_task = await self.__get_random_except(
                len(config.LEARN['Listen']) - 1, task)
        else:
            new_task = randint(0, len(config.LEARN['Listen']) - 1)

        inline_keyboard.add(
            InlineKeyboardButton(
                text='Посмотреть ответы',
                callback_data=f'listen_answers_{new_task}'))

        if await TGFile.exist.vid(config.LEARN['Listen'][new_task]['video']):
            await bot.send_video(
                chat_id=chat_id,
                video=await TGFile.get.file_id(
                    config.LEARN['Listen'][new_task]['video']),
                reply_markup=inline_keyboard)
        else:
            send_msg = await bot.send_video(
                chat_id=chat_id,
                video=types.InputFile(
                    f'data/vid/{config.LEARN["Listen"][new_task]["video"]}'),
                reply_markup=inline_keyboard)

            await TGFile.add.vid(
                config.LEARN['Listen'][new_task]['video'],
                send_msg.video.file_id)

    async def listen_answers(self, chat_id: int, message_id: int, task: int):
        """
        Use this method to edit a message on the listen task answers

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`
        :param task: Last task number
        :type task: :obj:`int`

        :return: On success, returns edited message
        :rtype: :obj:`types.Message`
        """
        inline_keyboard = InlineKeyboardMarkup()
        answers = ''

        inline_keyboard.add(
            InlineKeyboardButton(
                text='Продолжить »',
                callback_data=f'listen_{task}'))

        for qa in config.LEARN['Listen'][task]['QA']:
            answers += f'{qa}\n'

        await bot.edit_message_caption(
            chat_id, message_id,
            caption=answers,
            reply_markup=inline_keyboard)

    async def talk_task(self, chat_id: int, message_id, task: int = None):
        """
        Use this method to send a new talk task message

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`
        :param task: Last task number
        :type task: :obj:`int`

        :return: On success, returns a sent message
        :rtype: :obj:`types.Message`
        """
        inline_keyboard = InlineKeyboardMarkup()
        new_task: int

        await bot.edit_message_reply_markup(
            chat_id, message_id)

        if task is not None:
            new_task = await self.__get_random_except(
                len(config.LEARN['Talk']) - 1, task)
        else:
            new_task = randint(0, len(config.LEARN['Talk']) - 1)

        config.ANSWERS[chat_id] = new_task

        inline_keyboard.add(
            InlineKeyboardButton(
                text='Написать ответ',
                callback_data=f'talk_answer_{new_task}'))

        if await TGFile.exist.img(config.LEARN['Talk'][new_task]):
            await bot.send_photo(
                chat_id=chat_id,
                photo=await TGFile.get.file_id(
                    config.LEARN['Talk'][new_task]),
                reply_markup=inline_keyboard)
        else:
            send_msg = await bot.send_photo(
                chat_id=chat_id,
                photo=types.InputFile(
                    f'data/img/{config.LEARN["Talk"][new_task]}'),
                reply_markup=inline_keyboard)

            await TGFile.add.img(
                config.LEARN['Talk'][new_task],
                send_msg.photo[-1].file_id)

    async def talk_answer_start(self, chat_id: int, message_id: int):
        """
        Use this method to activate talk answer

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`

        :return: On success, returns an edited message
        :rtype: :obj:`types.Message`
        """
        return await bot.edit_message_caption(
            chat_id, message_id,
            caption='Напиши ответ и я передам его на проверку!')

    async def talk_answer_end(self, chat_id: int, message_id: int, answer: str, state: FSMContext):
        """
        Use this method to save the user talk task answer

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`
        :param answer: Answer text
        :type answer: :obj:`str`
        :param state: Active state
        :type state: :obj:`FSMContext`

        :return: On success, returns a sent message
        :rtype: :obj:`types.Message`
        """
        await state.finish()

        inline_keyboard = InlineKeyboardMarkup()

        if chat_id in config.ANSWERS:
            await Database.answers.add(
                chat_id, message_id, 'talk',
                config.ANSWERS[chat_id], answer)

            inline_keyboard.add(
                InlineKeyboardButton(
                    text='Продолжить »',
                    callback_data=f'talk_{config.ANSWERS[chat_id]}'))

            del config.ANSWERS[chat_id]

            return await bot.send_message(
                chat_id, 'Отлично! Твой ответ передан на проверку.',
                reply_markup=inline_keyboard)

        return await bot.send_message(
            chat_id, text='Похоже что-то пошло не так. 😔')

    async def write_task(self, chat_id: int, message_id, task: int = None):
        """
        Use this method to send a new write task message

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`
        :param task: Last task number
        :type task: :obj:`int`

        :return: On success, returns a sent message
        :rtype: :obj:`types.Message`
        """
        inline_keyboard = InlineKeyboardMarkup()
        new_task: int

        await bot.edit_message_reply_markup(
            chat_id, message_id)

        if task is not None:
            new_task = await self.__get_random_except(
                len(config.LEARN['Write']) - 1, task)
        else:
            new_task = randint(0, len(config.LEARN['Write']) - 1)

        config.ANSWERS[chat_id] = new_task

        inline_keyboard.add(
            InlineKeyboardButton(
                text='Написать ответ',
                callback_data=f'write_answer_{new_task}'))

        await bot.send_message(
            chat_id=chat_id,
            text=config.LEARN['Write'][new_task],
            reply_markup=inline_keyboard)

    async def write_answer_start(self, chat_id: int, message_id: int):
        """
        Use this method to activate write task answer

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`
        :param task: Last task number
        :type task: :obj:`int`

        :return: On success, returns a sent or edited message
        :rtype: :obj:`typing.Union[types.Message]`
        """
        await bot.edit_message_reply_markup(
            chat_id, message_id)

        await bot.send_message(
            chat_id, text='Напиши ответ и я передам его на проверку!',
            reply_to_message_id=message_id)

    async def write_answer_end(self, chat_id: int, message_id: int, answer: str, state: FSMContext):
        """
        Use this method to save the user write task answer

        :param chat_id: Chat ID
        :type chat_id: :obj:`int`
        :param message_id: ID of the chat message
        :type message_id: :obj:`int`
        :param task: Last task number
        :type task: :obj:`int`

        :return: On success, returns a sent or edited message
        :rtype: :obj:`typing.Union[types.Message]`
        """
        await state.finish()

        inline_keyboard = InlineKeyboardMarkup()

        if chat_id in config.ANSWERS:
            await Database.answers.add(
                chat_id, message_id, 'write',
                config.ANSWERS[chat_id], answer)

            inline_keyboard.add(
                InlineKeyboardButton(
                    text='Продолжить »',
                    callback_data=f'write_{config.ANSWERS[chat_id]}'))

            del config.ANSWERS[chat_id]

            return await bot.send_message(
                chat_id, 'Отлично! Твой ответ передан на проверку.',
                reply_markup=inline_keyboard)

        return await bot.send_message(
            chat_id, text='Похоже что-то пошло не так. 😔')
