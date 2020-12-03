import logging
import random

from django.contrib import admin

from santapp.models import User


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


_distribute_to_participants.short_description = "Distribute to participants"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'address', 'wishlist', 'present_to']
    actions = [_distribute_to_participants]


admin.site.register(User, ArticleAdmin)
