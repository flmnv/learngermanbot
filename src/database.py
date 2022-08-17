import sqlite3


class UserAnswersTable:
    """
    Base user answers table class
    """

    async def add(chat_id: int, message_id: int,
                  task_type: str, task_num: int,
                  answer_text: str):
        """
        Use this method to add user answer

        :param user_id: Unique Telegram user identifier
        :type user_id: :obj:`int``
        """
        connect = sqlite3.connect('db/users.db')
        cursor = connect.cursor()

        insert_values = [chat_id, message_id,
                         task_type, task_num,
                         answer_text]

        cursor.execute(
            '''
            INSERT INTO user_answers(
                chat_id, message_id, task_type, task_num, answer)
            VALUES(?, ?, ?, ?, ?)
            ''',
            insert_values)

        connect.commit()

    async def get_answer():
        """
        Use this method to get user answer

        :return: On success, returns answer data
        :rtype: :obj:`typing.Union[None, tuple]`
        """
        connect = sqlite3.connect('db/users.db')
        cursor = connect.cursor()

        cursor.execute(
            '''
            SELECT ID, chat_id, message_id, task_type, task_num, answer FROM user_answers
            LIMIT 1
            ''')

        answer = cursor.fetchone()

        return answer

    async def remove(ID: int):
        """
        Use this method to remove answer

        :param ID: Answer ID
        :type ID: :obj:`int``
        """
        connect = sqlite3.connect('db/users.db')
        cursor = connect.cursor()

        insert_values = [ID]

        cursor.execute(
            '''
            DELETE FROM user_answers
            WHERE ID = ?
            ''',
            insert_values)

        connect.commit()


class AdminsTable:
    """
    Base admins table class
    """

    async def add(user_id: int):
        """
        Use this method to add admin

        :param user_id: Unique Telegram user identifier
        :type user_id: :obj:`int``
        """
        connect = sqlite3.connect('db/users.db')
        cursor = connect.cursor()

        insert_values = [user_id]

        cursor.execute(
            '''
            INSERT INTO admins(user_id)
            VALUES(?)
            ''',
            insert_values)

        connect.commit()

    async def remove(user_id: int):
        """
        Use this method to remove admin

        :param user_id: Unique Telegram user identifier
        :type user_id: :obj:`int``
        """
        connect = sqlite3.connect('db/users.db')
        cursor = connect.cursor()

        insert_values = [user_id]

        cursor.execute(
            '''
            DELETE FROM admins
            WHERE user_id = ?
            ''',
            insert_values)

        connect.commit()

    async def exist(user_id: int):
        """
        Use this method to check user_id

        :param user_id: Unique Telegram user identifier
        :type user_id: :obj:`int``

        :return: On success, returns True
        :rtype: :obj:`bool`
        """
        connect = sqlite3.connect('db/users.db')
        cursor = connect.cursor()

        insert_values = [user_id]

        cursor.execute(
            '''
            SELECT ID FROM admins
            WHERE user_id = ?
            ''',
            insert_values)

        id = cursor.fetchone()

        if id is not None:
            return True

        return False


class Database:
    """
    Base database class
    """

    admins = AdminsTable
    answers = UserAnswersTable

    async def create():
        """
        Use this method to create a database and its tables
        """
        connect = sqlite3.connect('db/users.db')
        cursor = connect.cursor()

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            admins(
                ID INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL)
            ''')

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            user_answers(
                ID INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                task_type TEXT NOT NULL,
                task_num INTEGER NOT NULL,
                answer TEXT NOT NULL)
            ''')

        connect.commit()
