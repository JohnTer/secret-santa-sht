import logging
from django.db import models
from django_fsm import FSMField, transition
from asgiref.sync import sync_to_async


class UserStateEnum(object):
    TUTORIAL = 'tutorial'
    MENU = 'menu'
    WISHLIST = 'wishlist'
    ADDRESS = 'address'
    FULL_NAME = 'fullname'


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    text = models.CharField(max_length=2048)
    attachment_filename = models.CharField(max_length=64)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    vk_id = models.IntegerField(unique=True)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    registration_time = models.DateTimeField(auto_now_add=True)

    friend_available = models.BooleanField(default=False)
    address = models.CharField(max_length=256, null=True, default=None)
    wishlist = models.CharField(max_length=2048, null=True, default=None)
    full_name = models.CharField(max_length=256, null=True, default=None)

    present_to = models.ForeignKey('self',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   default=None)

    state = FSMField(default=UserStateEnum.TUTORIAL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def create(cls, vk_user_id: int, first_name: str,
               last_name: str) -> 'User':
        return cls(first_name=first_name,
                   last_name=last_name,
                   vk_id=vk_user_id)

    @sync_to_async
    def get_friend(self):
        return self.present_to

    # FINITE STATE MACHINE AREA

    @transition(field=state,
                source=UserStateEnum.TUTORIAL,
                target=UserStateEnum.MENU)
    def tutorial_done(self):
        logging.info(
            f'User [vk_id={self.vk_id}] change state from [{UserStateEnum.TUTORIAL}] to [{UserStateEnum.MENU}]'
        )

    @transition(field=state,
                source=UserStateEnum.MENU,
                target=UserStateEnum.WISHLIST)
    def write_wishlist(self):
        logging.info(
            f'User [vk_id={self.vk_id}] change state from [{UserStateEnum.MENU}] to [{UserStateEnum.WISHLIST}]'
        )

    @transition(field=state,
                source=UserStateEnum.WISHLIST,
                target=UserStateEnum.MENU)
    def write_wishlist_done(self):
        logging.info(
            f'User [vk_id={self.vk_id}] change state from [{UserStateEnum.WISHLIST}] to [{UserStateEnum.MENU}]'
        )

    @transition(field=state,
                source=UserStateEnum.MENU,
                target=UserStateEnum.ADDRESS)
    def write_address(self):
        logging.info(
            f'User [vk_id={self.vk_id}] change state from [{UserStateEnum.WISHLIST}] to [{UserStateEnum.ADDRESS}]'
        )

    @transition(field=state,
                source=UserStateEnum.ADDRESS,
                target=UserStateEnum.MENU)
    def write_address_done(self):
        logging.info(
            f'User [vk_id={self.vk_id}] change state from [{UserStateEnum.ADDRESS}] to [{UserStateEnum.MENU}]'
        )

    @transition(field=state,
                source=UserStateEnum.MENU,
                target=UserStateEnum.FULL_NAME)
    def write_full_name(self):
        logging.info(
            f'User [vk_id={self.vk_id}] change state from [{UserStateEnum.WISHLIST}] to [{UserStateEnum.FULL_NAME}]'
        )

    @transition(field=state,
                source=UserStateEnum.FULL_NAME,
                target=UserStateEnum.MENU)
    def write_full_name_done(self):
        logging.info(
            f'User [vk_id={self.vk_id}] change state from [{UserStateEnum.FULL_NAME}] to [{UserStateEnum.MENU}]'
        )
