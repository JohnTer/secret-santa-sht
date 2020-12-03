from dataclasses import dataclass

from ..models import User


@dataclass
class UserMessage(object):
    text: str
    payload: dict[str, str]
    message_id: str

    user: User
