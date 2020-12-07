import os
from typing import Union

from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards import Template
from vkwave.bots.utils.keyboards import ButtonColor

from ..models import User, UserStateEnum
from secret_santa import settings
from santapp.vk_utils.message import get_photo_id


class BeforeGameTemplate(object):
    @staticmethod
    async def get_template(user: User) -> str:
        photo_path_first: str = os.path.join(settings.STATIC_PATH, 'hse1.jpg')
        photo_id_first: str = await get_photo_id(user.vk_id, photo_path_first)

        color: Union[ButtonColor.PRIMARY, ButtonColor.POSITIVE, None] = None

        input_template = Template(
            title="Расскажи немного о себе!",
            description=f"{user.first_name} {user.last_name}",
            photo_id=photo_id_first)

        color = ButtonColor.PRIMARY if user.address is None else ButtonColor.POSITIVE
        input_template.add_text_button("Заполнить адрес",
                                       color=color,
                                       payload={'menu': 'write_address'})

        color = ButtonColor.PRIMARY if user.wishlist is None else ButtonColor.POSITIVE
        input_template.add_text_button("Заполнить вишлист",
                                       color=color,
                                       payload={'menu': 'write_wishlist'})

        color = ButtonColor.PRIMARY if user.full_name is None else ButtonColor.POSITIVE
        input_template.add_text_button("Заполнить ФИО",
                                       color=color,
                                       payload={'menu': 'write_full_name'})

        return Template.generate_carousel(input_template)


class OnGameTemplate(object):
    @staticmethod
    async def get_template(user: User) -> str:
        photo_path_second: str = os.path.join(settings.STATIC_PATH, 'hse2.jpg')
        photo_id_second: str = await get_photo_id(user.vk_id,
                                                  photo_path_second)

        friend: Optional[User] = await user.get_friend()

        friend_template = Template(title="Твой друг!",
                                   description=f"{friend.full_name}",
                                   photo_id=photo_id_second)

        friend_template.add_text_button("Адрес друга",
                                        color=ButtonColor.SECONDARY,
                                        payload={'menu': 'get_address'})
        friend_template.add_text_button("Вишлист друга",
                                        payload={'menu': 'get_wishlist'})
        friend_template.add_text_button("ФИО друга",
                                        payload={'menu': 'get_full_name'})

        return Template.generate_carousel(friend_template)


class BackKeyboard(object):
    @staticmethod
    def get_keyboard() -> str:
        keyboard = Keyboard(one_time=True)
        keyboard.add_text_button(text="Назад")
        return keyboard.get_keyboard()
