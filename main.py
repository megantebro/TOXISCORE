
import discord
from discord import app_commands
from dotenv import load_dotenv
import os

from ai import judge_message
from db import get_avg_userscore, save_message



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv()
TOKEN = os.getenv("TOKEN")

@client.event
async def on_ready():
    await tree.sync()
    print("ready")

@client.event
async def on_message(message:discord.Message):
    if(message.author == client.user):return
    user = message.author
    content = message.content



    print(f"{message.author.display_name}:{message.content}")
    score = await judge_message(content)
    save_message(str(user.id),user.display_name,content,score)


    if score > 0:
        await message.channel.send(f"⚠ 暴言スコア: **{score}**")


@tree.command(name="avg_toxiscore",description="ユーザーの平均暴言スコアを取得します")
async def avg_toxiscore(interaction:discord.Interaction,user:discord.Member = None):
    if(user == None):
        user = interaction.user
    avg_score = get_avg_userscore(user.id)
    await interaction.response.send_message(avg_score)

client.run(TOKEN)




