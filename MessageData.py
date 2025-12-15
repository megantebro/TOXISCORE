
from discord import User


class MessageData:
    def __init__(self, user,guild_id,content):
        self.user = user
        self.content = content
        self.guild_id = guild_id