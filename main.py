

import asyncio
import json
import time
import discord
from discord import User, app_commands
from dotenv import load_dotenv
import os

from MessageData import MessageData
from ai import judge_message
from db import save_messages
import commands


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
commands.setup(tree)
queue:list[MessageData] = []

user_last_messagetime:dict[User,float] = {}

load_dotenv()
TOKEN = os.getenv("TOKEN")

@client.event
async def on_ready():
    await tree.sync()

    print("ready")
    await consume_queue()

@client.event
async def on_message(message:discord.Message):
    if(message.author == client.user):return
    if(is_channel_exclude(message.channel.id)):return
    if(message.author in user_last_messagetime):
        if(time.time() - user_last_messagetime[message.author] < 5):return
    global queue

    user = message.author
    content = message.content
    msg_data = MessageData(user,content)
    queue.append(msg_data)

    user_last_messagetime[user] = time.time()
    print(f"{message.author.display_name}:{message.content}")

def is_channel_exclude(channel_id:int) -> bool:
    with open("config.json","r") as file:
        json_data = json.load(file)
    return channel_id in json_data["exclude_channel_ids"]


async def consume_queue():
    while True:
        global queue
        if len(queue) != 0:
            scores = await judge_message(queue)
            save_messages(queue,scores)
            queue = []
        await asyncio.sleep(30)

client.run(TOKEN)




