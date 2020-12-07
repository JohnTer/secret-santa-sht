import logging
import os
from typing import Optional

from asgiref.sync import sync_to_async

from vkwave.bots.utils.keyboards import Template, ButtonColor
from vkwave.bots import Keyboard

from secret_santa import settings

from ..message import UserMessage
from ..vk_utils.message import send_message, get_photo_id
from ..models import User


class BaseContext(object):
    def __init__(self):
        self.text = None
        self.template = None

    async def incoming_handler(self) -> None:
        raise NotImplementedError

    async def outcoming_handler(self) -> None:
        raise NotImplementedError

    async def _invalid_input_handler(self) -> None:
        raise NotImplementedError

    def _is_valid(self) -> None:
        raise NotImplementedError


class WrittingWishlistContext(BaseContext):
    def __init__(self):
        self._to_context_text = "Напиши свой вишлист, чтобы Штайный Санта знал, что тебе подарить!\n\n"
        self._from_context_text = "Твой вишлист успешно записан!"
        self._message_not_valid_text = "Вишлист не может быть пустым!"

    def _get_keyboard(self) -> str:
        kb: Keyboard = Keyboard(one_time=True)
        kb.add_text_button(text="Назад")
        return kb.get_keyboard()

    async def on_context_handler(self, message: UserMessage) -> bool:
        if message.text == '':
            await self._invalid_input_handler(message.user)
            return True

        wishlist: str = message.text
        user: User = message.user
        user.write_wishlist_done()

        if wishlist != "Назад":
            user.wishlist = wishlist
            await sync_to_async(message.user.save)()
            await self._from_contex_handler(user)
        else:
            await sync_to_async(message.user.save)()

        return True

    async def to_context_handler(self, user: User) -> None:
        wishlist: Optional[str] = user.wishlist
        text: str = self._to_context_text
        if wishlist is not None:
            text += "Ранее ты указал(а): {}".format(wishlist)
        await send_message(peer_id=user.vk_id,
                           message=text,
                           keyboard=self._get_keyboard())

    async def _from_contex_handler(self, user: User) -> None:
        await send_message(peer_id=user.vk_id, message=self._from_context_text)
        logging.info(f'User [{user.vk_id}] completed writing the wishlist')

    async def _invalid_input_handler(self, user: User) -> None:
        await send_message(peer_id=user.vk_id,
                           message=self._message_not_valid_text)


class WrittingAddressContext(WrittingWishlistContext):
    def __init__(self):
        self._to_context_text = "Напиши свой адрес, чтобы Штайный Санта смог отправить тебе подарок!\n\n"
        self._from_context_text = "Твой адрес успешно записан!"
        self._message_not_valid_text = "Адрес не может быть пустым!"

    def _get_keyboard(self) -> str:
        kb: Keyboard = Keyboard(one_time=True)
        kb.add_text_button(text="Назад")
        return kb.get_keyboard()

    async def on_context_handler(self, message: UserMessage) -> bool:
        if message.text == '':
            await self._invalid_input_handler(message.user)
            return True

        address: str = message.text
        user: User = message.user
        user.write_address_done()

        if address != "Назад":
            user.address = address
            await sync_to_async(message.user.save)()
            await self._from_contex_handler(user)
        else:
            await sync_to_async(message.user.save)()

        return True

    async def to_context_handler(self, user: User) -> None:
        address: Optional[str] = user.address
        text: str = self._to_context_text
        if address is not None:
            text += "Ранее ты указал(а): {}".format(address)
        await send_message(peer_id=user.vk_id,
                           message=text,
                           keyboard=self._get_keyboard())

    async def _from_contex_handler(self, user: User) -> None:
        await send_message(peer_id=user.vk_id, message=self._from_context_text)
        logging.info(f'User [{user.vk_id}] completed writing the address')

    async def _invalid_input_handler(self, user: User) -> None:
        await send_message(peer_id=user.vk_id,
                           message=self._message_not_valid_text)


class WrittingFullNameContext(WrittingWishlistContext):
    def __init__(self):
        self._to_context_text = "Напиши свое ФИО, твой подарок нашел тебя!\n\n"
        self._from_context_text = "Твое ФИО успешно записано!"
        self._message_not_valid_text = "ФИО не может быть пустым!"

    def _get_keyboard(self) -> str:
        kb: Keyboard = Keyboard(one_time=True)
        kb.add_text_button(text="Назад")
        return kb.get_keyboard()

    async def on_context_handler(self, message: UserMessage) -> bool:
        if message.text == '':
            await self._invalid_input_handler(message.user)
            return True

        full_name: str = message.text
        user: User = message.user
        user.write_full_name_done()

        if full_name != "Назад":
            user.full_name = full_name
            await sync_to_async(message.user.save)()
            await self._from_contex_handler(user)
        else:
            await sync_to_async(message.user.save)()

        return True

    async def to_context_handler(self, user: User) -> None:
        full_name: Optional[str] = user.full_name
        text: str = self._to_context_text
        if full_name is not None:
            text += "Ранее ты указал(а): {}".format(full_name)
        await send_message(peer_id=user.vk_id,
                           message=text,
                           keyboard=self._get_keyboard())

    async def _from_contex_handler(self, user: User) -> None:
        await send_message(peer_id=user.vk_id, message=self._from_context_text)
        logging.info(f'User [{user.vk_id}] completed writing the full_name')

    async def _invalid_input_handler(self, user: User) -> None:
        await send_message(peer_id=user.vk_id,
                           message=self._message_not_valid_text)


class MenuContext(BaseContext):
    def __init__(self, writting_address_ctx: WrittingAddressContext,
                 writting_wishlist_ctx: WrittingWishlistContext):

        self.writting_address_ctx: WrittingAddressContext = writting_address_ctx
        self.writting_wishlist_ctx: WrittingWishlistContext = writting_wishlist_ctx

        self._main_text: str = "До нового года осталось совсем чуть-чуть!"

        self._no_friends_text: str = "Еще пока нельзя посмотреть, кто твой друг."

        self._no_address_text: str = "Твой друг еще не заполнил адрес."

        self._no_wishlist_text: str = "Твой друг еще не заполнил вишлист."

        self._no_full_name_text: str = "Твой друг еще не заполнил ФИО."

        self._unknown_message_text: str = "Чтобы совершить какие-либо действия, воспользуйся кнопками на карточках."

    async def _get_message_template(self, user: User) -> Template:
        photo_path_first: str = os.path.join(settings.STATIC_PATH, 'hse1.jpg')
        photo_id_first: str = await get_photo_id(user.vk_id, photo_path_first)
        input_template = Template(
            title="Расскажи немного о себе!",
            description=f"{user.first_name} {user.last_name}",
            photo_id=photo_id_first)

        input_template.add_text_button("Заполнить адрес",
                                       color=ButtonColor.SECONDARY,
                                       payload={'menu': 'write_address'})
        input_template.add_text_button("Заполнить вишлист",
                                       payload={'menu': 'write_wishlist'})
        input_template.add_text_button("Заполнить ФИО",
                                       payload={'menu': 'write_full_name'})

        friend: Optional[User] = await user.get_friend()
        friend_description: str = "Распределение уже скоро!" if friend is None or not user.friend_available else f"{friend.first_name} {friend.last_name}"

        photo_path_second: str = os.path.join(settings.STATIC_PATH, 'hse2.jpg')
        photo_id_second: str = await get_photo_id(user.vk_id,
                                                  photo_path_second)

        friend_template = Template(
            title="Твой друг!",
            description=friend_description,
            #photo_id="222556886_457240311_0b1f8444fd9d841bed")
            photo_id=photo_id_second)

        friend_template.add_text_button("Адрес друга",
                                        color=ButtonColor.SECONDARY,
                                        payload={'menu': 'get_address'})
        friend_template.add_text_button("Вишлист друга",
                                        payload={'menu': 'get_wishlist'})
        friend_template.add_text_button("ФИО друга",
                                        payload={'menu': 'get_full_name'})

        return Template.generate_carousel(input_template, friend_template)

    async def on_context_handler(self, message: UserMessage) -> bool:
        if not self._is_valid(message):
            return await self._unknown_message_handler(message)

        button_type: str = message.payload['menu']
        next_state: bool = False

        if button_type == 'get_address':
            next_state = await self._get_address_handler(message.user)
        elif button_type == 'get_wishlist':
            next_state = await self._get_wishlist_handler(message.user)
        elif button_type == 'get_full_name':
            next_state = await self._get_full_name_handler(message.user)
        elif button_type == 'write_wishlist':
            next_state = await self._write_wishlist_handler(message.user)
        elif button_type == 'write_address':
            next_state = await self._write_address_handler(message.user)
        elif button_type == 'write_full_name':
            next_state = await self._write_full_name_handler(message.user)
        else:
            next_state = await self._unknown_message_handler(message)

        return next_state

    async def to_context_handler(self, user: User) -> None:
        await send_message(peer_id=user.vk_id,
                           template=await self._get_message_template(user),
                           message=self._main_text)

    async def _get_address_handler(self, user: User) -> bool:
        friend: Optional[User] = await user.get_friend()
        if friend is None or not user.friend_available:
            await send_message(peer_id=user.vk_id,
                               message=self._no_friends_text)
            return False

        message: str = friend.address or self._no_address_text

        logging.info(f'User [{user.vk_id}] get friends address')

        await send_message(peer_id=user.vk_id, message=message)
        return False

    async def _get_wishlist_handler(self, user: User) -> bool:
        friend: Optional[User] = await user.get_friend()
        if friend is None or not user.friend_available:
            await send_message(peer_id=user.vk_id,
                               message=self._no_friends_text)
            return False

        message: str = friend.wishlist or self._no_wishlist_text

        await send_message(peer_id=user.vk_id, message=message)

        logging.info(f'User [{user.vk_id}] get friends fishlist')
        return False

    async def _get_full_name_handler(self, user: User) -> bool:
        friend: Optional[User] = await user.get_friend()
        if friend is None or not user.friend_available:
            await send_message(peer_id=user.vk_id,
                               message=self._no_friends_text)
            return False

        message: str = friend.full_name or self._no_full_name_text

        await send_message(peer_id=user.vk_id, message=message)

        logging.info(f'User [{user.vk_id}] get friends full_name')
        return False

    async def _write_wishlist_handler(self, user: User) -> bool:
        user.write_wishlist()
        await sync_to_async(user.save)()
        return True

    async def _write_full_name_handler(self, user: User) -> bool:
        user.write_full_name()
        await sync_to_async(user.save)()
        return True



    async def _write_address_handler(self, user: User) -> bool:
        user.write_address()
        await sync_to_async(user.save)()
        return True

    async def _unknown_message_handler(self, message: UserMessage) -> bool:
        await send_message(message.user.vk_id, self._unknown_message_text)
        return True

    def _is_valid(self, message: UserMessage):
        return (message.payload is not None) and ('menu' in message.payload)


class TutorialContext(BaseContext):
    def __init__(self):
        self._greeting_text: str = "Привет!"
        self._from_context_text: str = """Мы рады приветствовать тебя на Штайном Санте! Основные правила ты уже знаешь, давай я расскажу тебе о том, как пользоваться этим ботом! 

В разделе “заполнить адрес” ты можешь ввести адрес места, куда нужно будет отправить твой подарок. В этом же разделе можно посмотреть адрес, который ты вводил последним и в случае чего изменить его. 

В разделе “заполнить вишлист” отправь список того, чтобы ты хотел(а) получить в посылке. Список может быть только текстовой (+ смайлы при необходимости). В этом же разделе можно посмотреть тот вишлист, который ты заполнил(а) ранее. В случае чего, ты можешь его здесь же и изменить. 

В разделе “адрес друга” и “вишлист друга” ты можешь посмотреть то, что заполнил человек, которому ты будешь собирать подарок. 

Если у тебя возникнут какие-нибудь вопросы, то https://vk.com/wateren на них ответит! """

    async def on_context_handler(self, message: UserMessage) -> bool:
        user: User = message.user

        await send_message(peer_id=user.vk_id, message=self._greeting_text)

        user.tutorial_done()

        await sync_to_async(message.user.save)()
        await self._from_contex_handler(user)

        return True

    async def to_context_handler(self, user: User) -> None:
        pass

    async def _from_contex_handler(self, user: User) -> None:
        await send_message(peer_id=user.vk_id, message=self._from_context_text)
        logging.info(f'User [{user.vk_id}] completed the tutorial')
