import json
import os

import src.config as config


class TGFileGet:
    """
    Base get Telegram file class
    """

    async def file_id(file: str):
        """
        Use this method to get file id

        :param file: File name
        :type file: :obj:`str`

        :return: Returns file Telegram id
        :rtype: :obj:`str`
        """
        return config.FILES[file]['id']


class TGFileAdd:
    """
    Base add Telegram file class
    """

    async def img(file: str, id: str):
        """
        Use this method to add image file id

        :param file: File name
        :type file: :obj:`str`
        :param id: File identifier
        :type id: :obj:`str`
        """
        config.FILES[file] = {}
        config.FILES[file]['id'] = id
        config.FILES[file]['mtime'] = os.path.getmtime(f'data/img/{file}')

        with open(f'data/json/id.json', 'w', encoding='utf-8') as id_file:
            json.dump(obj=config.FILES, fp=id_file,
                      ensure_ascii=False, indent=4)

    async def vid(file: str, id: str):
        """
        Use this method to add video file id

        :param file: File name
        :type file: :obj:`str`
        :param id: File identifier
        :type id: :obj:`str`
        """
        config.FILES[file] = {}
        config.FILES[file]['id'] = id
        config.FILES[file]['mtime'] = os.path.getmtime(f'data/vid/{file}')

        with open(f'data/json/id.json', 'w', encoding='utf-8') as id_file:
            json.dump(obj=config.FILES, fp=id_file,
                      ensure_ascii=False, indent=4)


class TGFileExist:
    """
    Base exist Telegram file class
    """

    async def img(file: str):
        """
        Use this method to find out if the image file id already exists

        :param file: File name
        :type file: :obj:`str`

        :return: Returns True if the image file id exists, otherwise False
        :rtype: :obj:`bool`
        """
        if (file in config.FILES and
            'id' in config.FILES[file] and
            'mtime' in config.FILES[file] and
                os.path.getmtime(f'data/img/{file}') == config.FILES[file]['mtime']):
            return True

        return False

    async def vid(file: str):
        """
        Use this method to find out if the video file id already exists

        :param file: File name
        :type file: :obj:`str`

        :return: Returns True if the video file id exists, otherwise False
        :rtype: :obj:`bool`
        """
        if (file in config.FILES and
            'id' in config.FILES[file] and
            'mtime' in config.FILES[file] and
                os.path.getmtime(f'data/vid/{file}') == config.FILES[file]['mtime']):
            return True

        return False


class TGFile:
    """
    Base Telegram file class
    """

    exist = TGFileExist
    add = TGFileAdd
    get = TGFileGet
