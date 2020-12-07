import logging
from typing import Union, Optional, Awaitable

import orjson
import aiohttp
from asgiref.sync import sync_to_async

from ..message.message import UserMessage
from ..vk_utils.message import get_user_name, SingletonMeta
from .contexts import MenuContext, WrittingAddressContext, WrittingWishlistContext, TutorialContext, WrittingFullNameContext
from ..models import User, UserStateEnum


class ContextManager(object):
    def __init__(self):
        wishlist_ctx: WrittingWishlistContext = WrittingWishlistContext()
        address_ctx: WrittingAddressContext = WrittingAddressContext()
        menu_ctx: MenuContext = MenuContext(address_ctx, wishlist_ctx)
        tutorial_ctx: TutorialContext = TutorialContext()
        write_full_name_ctx: WrittingFullNameContext = WrittingFullNameContext(
        )

        self.contexts: dict[str,
                            Union[MenuContext, WrittingAddressContext,
                                  WrittingWishlistContext]] = {
                                      UserStateEnum.TUTORIAL: tutorial_ctx,
                                      UserStateEnum.MENU: menu_ctx,
                                      UserStateEnum.ADDRESS: address_ctx,
                                      UserStateEnum.WISHLIST: wishlist_ctx,
                                      UserStateEnum.FULL_NAME:
                                      write_full_name_ctx
                                  }

    async def _get_user_info(self, vk_id: int) -> tuple[str, str]:
        first_name: str
        last_name: str

        first_name, last_name = await get_user_name(vk_id)

        return first_name, last_name

    async def _get_user_by_id(self, user_id: int) -> Optional[User]:
        user: Optional[User] = None

        try:
            user = await sync_to_async(User.objects.get)(vk_id=user_id)
        except User.DoesNotExist:
            first_name, last_name = await self._get_user_info(user_id)
            user = User.create(vk_user_id=user_id,
                               first_name=first_name,
                               last_name=last_name)
            await sync_to_async(user.save)()
        except Exception:
            logging.exception(f'Couldnt get the user[vk_id={user_id}]')
            return None
        return user

    async def get_message_object(self, json_data: dict) -> UserMessage:
        json_message: str = json_data['object']['message']

        user_id: int = json_message['from_id']
        text: str = json_message['text']
        payload: dict[str, str] = orjson.loads(
            json_message['payload']) if 'payload' in json_message else None
        message_id: int = json_message['id']

        user: User = await self._get_user_by_id(user_id)

        return UserMessage(text, payload, message_id, user)

    async def process(self, json_request_data: dict) -> None:
        message: UserMessage = await self.get_message_object(json_request_data)
        await self._run_context_manager(message)

    async def _run_context_manager(self, message: UserMessage) -> None:
        state: str = message.user.state

        logging.info(
            f'The user [vk_id={message.user.vk_id}] has the state={state}')

        ctx: Union[MenuContext, WrittingAddressContext,
                   WrittingWishlistContext] = self.contexts[state]

        next_state: bool = await ctx.on_context_handler(message)

        if next_state:
            state: str = message.user.state
            next_ctx: Union[MenuContext, WrittingAddressContext,
                            WrittingWishlistContext] = self.contexts[state]
            await next_ctx.to_context_handler(message.user)
