import logging
import random

from django.contrib import admin
from asgiref.sync import async_to_sync

from santapp.models import User, Message
from .vk_utils.message import send_message


def _distribute_to_participants(modeladmin, request, queryset) -> None:
    def link_to_participants(user_list: list[User]) -> None:
        if len(user_list) < 2:
            return
        random.shuffle(user_list)
        user_list[-1].present_to = user_list[0]
        user_list[-1].save()
        for i in range(len(user_list) - 1):
            user_list[i].present_to = user_list[i + 1]
            user_list[i].save()

    user_list: list[User] = list(queryset)
    link_to_participants(user_list)
    logging.info('The distribution of completed')

    result: list[str] = [str(user) for user in user_list]

    logging.info(f'The distribution is: {result}')


def _open_game(modeladmin, request, queryset) -> None:
    user_list: list[User] = list(queryset)
    for user in user_list:
        user.friend_available = True
        user.save()


def _close_game(modeladmin, request, queryset) -> None:
    user_list: list[User] = list(queryset)
    for user in user_list:
        user.friend_available = False
        user.save()


def _mailling(modeladmin, request, queryset) -> None:
    user_list: list[User] = list(queryset)

    message: Message = Message.objects.get(name='mail')
    print(message, user_list)
    for user in user_list:
        async_to_sync(send_message)(user.vk_id, message.text)


_distribute_to_participants.short_description = "Distribute to participants"
_open_game.short_description = "Open game"
_close_game.short_description = "Close game"
_mailling.short_description = "Send mail"


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'address', 'wishlist', 'present_to',
        'friend_available'
    ]
    actions = [_distribute_to_participants, _open_game, _close_game, _mailling]


class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'text']


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)