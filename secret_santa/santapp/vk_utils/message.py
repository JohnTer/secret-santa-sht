import random
import logging

from typing import Optional

import aiohttp

from vkwave.api import API, APIOptionsRequestContext
from vkwave.client import AIOHTTPClient
from vkwave.bots import PhotoUploader

from secret_santa import settings


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MediaCache(metaclass=SingletonMeta):
    def __init__(self):
        self._cache: dict[str, str] = {}

    def find(self, key: str) -> Optional[str]:
        return self._cache[key] if key in self._cache else None

    def update(self, key: str, value: str) -> None:
        if key not in self._cache:
            self._cache[key] = value


def _get_vk_api(session: aiohttp.ClientSession) -> APIOptionsRequestContext:
    return API(tokens=settings.API_KEY,
               clients=AIOHTTPClient(session=session)).get_context()


async def get_photo_id(vk_id: int, path: str) -> str:
    cache: MediaCache = MediaCache()
    picture_id: str = cache.find(path)
    if picture_id is not None:
        return picture_id
    try:
        async with aiohttp.ClientSession() as client:
            api: APIOptionsRequestContext = _get_vk_api(client)
            uploader: PhotoUploader = PhotoUploader(api)
            big_attachment: str = await uploader.get_attachment_from_path(
                peer_id=vk_id, file_path=path)
        picture_id = big_attachment[len('photo'):]
    except:
        logging.exception(
            f'The photo was not sent[vk_id={vk_id} path={path}]'
        )
    cache.update(path, picture_id)
    return picture_id


async def get_user_name(vk_id: int) -> tuple[str, str]:
    try:
        async with aiohttp.ClientSession() as client:
            api: APIOptionsRequestContext = _get_vk_api(client)
            response_list: list[dict] = await api.users.get(
                user_ids=[vk_id],
                fields=["first_name", "last_name"],
                return_raw_response=True)
            response: dict = response_list['response'][0]
            return response['first_name'], response['last_name']
    except:
        logging.exception(
            f'first and last name were not received[vk_id={vk_id}')
        return '', ''


async def send_message(peer_id: int,
                       message: str,
                       template: Optional[str] = None,
                       keyboard: Optional[str] = None) -> None:
    try:
        async with aiohttp.ClientSession() as client:
            api: APIOptionsRequestContext = _get_vk_api(client)
            await api.messages.send(peer_id=peer_id,
                                    message=message,
                                    template=template,
                                    keyboard=keyboard,
                                    random_id=random.getrandbits(64))
    except:
        logging.exception(
            f'The message was not sent[vk_id={peer_id} text={message}] keyboard={template} keyboard={keyboard}'
        )
