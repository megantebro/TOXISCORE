
from discord import User


class MessageData:
    def __init__(self, user, content):
        self.user = user
        self.content = content