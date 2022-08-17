from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext

import src.config as config
from src.config import bot
from src.database import Database
from src.learn import Learn
from src.tgfiles import TGFile


class UserState(StatesGroup):
    """
    Base user state class
    """

    talk_answer = State()
    write_answer = State()


class AdminState(StatesGroup):
    """
    Base admin state class
    """

    task_answer = State()


class Admin:
    """
    Base admin class
    """

    def __init__(self, user_id: int) -> None:
        """
        :param user_id: Unique Telegram user identifier
        :type user_id: :obj:`int`
        """
        self.id = user_id

    async def command_answer(self):
        """
        Use this method to admin command answer

        :return: On success, returns the sent message, otherwise False
        :rtype: :obj:`typing.Union[bool, types.Message]`
        """
        if not await Database.admins.exist(self.id):
            return False

        answer = await Database.answers.get_answer()

        if answer is None:
            return await bot.send_message(
                chat_id=self.id,
                text='Нет ответов, отправленных на проверку!')

        ID, chat_id, message_id, task_type, task_num, answer_text = answer

        if task_type == 'talk':
            msg_text = f'<b>Ответ:</b>\n{answer_text}'

            await AdminState.task_answer.set()
            config.ADMIN_ANSWERS[self.id] = [ID, chat_id, message_id]

            if await TGFile.exist.img(config.LEARN['Talk'][task_num]):
                return await bot.send_photo(
                    chat_id=self.id,
                    photo=await TGFile.get.file_id(
                        config.LEARN['Talk'][task_num]),
                    caption=msg_text,
                    parse_mode='html')
            else:
                send_msg = await bot.send_photo(
                    chat_id=self.id,
                    photo=types.InputFile(
                        f'data/img/{config.LEARN["Talk"][task_num]}'),
                    caption=msg_text,
                    parse_mode='html')

                await TGFile.add.img(
                    config.LEARN['Talk'][task_num],
                    send_msg.photo[-1].file_id)

                return send_msg
        elif task_type == 'write':
            msg_text = f'{config.LEARN["Write"][task_num]}\n\n<b>Ответ:</b>\n{answer_text}'

            await AdminState.task_answer.set()
            config.ADMIN_ANSWERS[self.id] = [ID, chat_id, message_id]

            return await bot.send_message(
                self.id, msg_text,
                parse_mode='html')

    async def answer(self, answer_text: str, state: FSMContext):
        """
        Use this method to send the administrator's answer to the user

        :param answer_text: Answer text
        :type answer_text: :obj:`str`
        :param state: Active state
        :type state: :obj:`FSMContext`

        :return: On success, returns the sent message
        :rtype: :obj:`types.Message`
        """
        await state.finish()

        if self.id not in config.ADMIN_ANSWERS:
            return await bot.send_message(
                chat_id=self.id,
                text='Похоже что-то пошло не так. 😔')

        await bot.send_message(
            chat_id=config.ADMIN_ANSWERS[self.id][1],
            text=answer_text,
            reply_to_message_id=config.ADMIN_ANSWERS[self.id][2])

        await Database.answers.remove(config.ADMIN_ANSWERS[self.id][0])
        del config.ADMIN_ANSWERS[self.id]


class User:
    """
    Base user class
    """

    def __init__(self, user_id: int) -> None:
        """
        :param user_id: Unique Telegram user identifier
        :type user_id: :obj:`int`
        """
        self.id = user_id
        self.admin = Admin(self.id)

    async def command_id(self):
        """
        Use this method to send the Telegram user ID to the user
        """
        await bot.send_message(
            chat_id=self.id,
            text=self.id)

    async def command_start(self):
        """
        Use this method to send the learn menu
        """
        learn = Learn()

        await learn.menu.send(self.id)

    async def write_task_start(self, message_id: int):
        """
        Use this method to start the write task
        """
        learn = Learn()

        await learn.menu.write_task(self.id, message_id)

    async def talk_task_start(self, message_id: int):
        """
        Use this method to start the talk task
        """
        learn = Learn()

        await learn.menu.talk_task(self.id, message_id)

    async def listen_task_start(self, message_id: int):
        """
        Use this method to start the listen task
        """
        learn = Learn()

        await learn.menu.listen_task(self.id, message_id)

    async def read_task_start(self, message_id: int):
        """
        Use this method to start the read task
        """
        learn = Learn()

        await learn.menu.read_task(
            self.id, message_id)

    async def talk_task(self, call: types.CallbackQuery):
        """
        Use this method to send the message with new random talk task
        or its answers.
        """
        learn = Learn()
        data = call.data.split('_')

        if len(data) == 2:
            await learn.menu.talk_task(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                task=int(data[1]))
        elif len(data) == 3:
            await UserState.talk_answer.set()

            await learn.menu.talk_answer_start(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id)

    async def talk_answer(self, message: types.Message, state: FSMContext):
        """
        Use this method to save the answer to the user's talk task
        """
        learn = Learn()

        await learn.menu.talk_answer_end(
            message.chat.id, message.message_id, message.text, state)

    async def write_task(self, call: types.CallbackQuery):
        """
        Use this method to send the message with new random write task
        or its answers.
        """
        learn = Learn()
        data = call.data.split('_')

        if len(data) == 2:
            await learn.menu.write_task(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                task=int(data[1]))
        elif len(data) == 3:
            await UserState.write_answer.set()

            await learn.menu.write_answer_start(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id)

    async def write_answer(self, message: types.Message, state: FSMContext):
        """
        Use this method to save the answer to the user's write task
        """
        learn = Learn()

        await learn.menu.write_answer_end(
            message.chat.id, message.message_id, message.text, state)

    async def listen_task(self, call: types.CallbackQuery):
        """
        Use this method to send the message with new random listen task
        or its answers.
        """
        learn = Learn()
        data = call.data.split('_')

        if len(data) == 2:
            await learn.menu.listen_task(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                task=int(data[1]))
        elif len(data) == 3:
            await learn.menu.listen_answers(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                task=int(data[2]))

    async def read_task(self, call: types.CallbackQuery):
        """
        Use this method to edit the message to the new random read task
        or its result.
        """
        learn = Learn()
        data = call.data.split('_')

        if len(data) == 2:
            await learn.menu.read_task(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                task=int(data[1]))
        elif len(data) == 3:
            task_answer: bool

            if data[2] == 'correct':
                task_answer = True
            else:
                task_answer = False

            await learn.menu.read_result(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                task=int(data[1]),
                answer=task_answer)

    async def command_info(self, message: types.Message):
        """
        Use this method to send information about the exam
        """
        learn = Learn()

        await learn.exam_info(message.chat.id)

    async def command_words(self, message: types.Message):
        """
        Use this method to send words with translation
        """
        learn = Learn()

        await learn.words(message.chat.id)

    async def words(self, call: types.CallbackQuery):
        """
        Use this method to change the page of words with translation
        """
        learn = Learn()
        page = int(call.data.split('_')[-1])

        await learn.words(
            call.message.chat.id, page,
            call.message.message_id)
