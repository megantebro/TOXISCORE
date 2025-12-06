

import discord
from discord import User, app_commands
from dotenv import load_dotenv
import os

from MessageData import MessageData
from ai import judge_message
from db import get_avg_userscore, get_server_avg, get_server_stddev,save_messages


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
msg_datas:list[MessageData] = []

load_dotenv()
TOKEN = os.getenv("TOKEN")

@client.event
async def on_ready():
    await tree.sync()
    print("ready")

@client.event
async def on_message(message:discord.Message):
    if(message.author == client.user):return
    global msg_datas

    user = message.author
    content = message.content
    msg_data = MessageData(user,content)
    msg_datas.append(msg_data)

    print(f"{message.author.display_name}:{message.content}")

    if len(msg_datas) < 10:return

    scores = await judge_message(msg_datas)
    save_messages(msg_datas,scores)
    msg_datas = []


@tree.command(name="avg_toxiscore",description="ユーザーの平均暴言スコアを取得します")
async def avg_toxiscore(interaction:discord.Interaction,user:discord.Member = None):
    if(user == None):
        user = interaction.user
    avg_score = get_avg_userscore(user.id)
    await interaction.response.send_message(avg_score)




@tree.command(
    name="toxicity_rank",
    description="サーバー平均と比較した治安影響スコアを表示します",
)
async def toxicity_rank(interaction: discord.Interaction, user: discord.Member = None):
    if user is None:
        user = interaction.user

    user_avg = get_avg_userscore(str(user.id))
    server_avg = get_server_avg()
    server_std = get_server_stddev()

    impact = user_avg - server_avg

    if server_std > 0:
        z = (user_avg - server_avg) / server_std
    else:
        z = 0

    msg = (
        f"📊 **{user.display_name} の治安スコア評価**\n\n"
        f"・あなたの平均暴言スコア：**{user_avg:.2f}**\n"
        f"・サーバー平均：**{server_avg:.2f}**\n"
        f"・治安への影響度：**{impact:+.2f}**\n"
        f"・偏差暴言スコア（Z値）：**{z:+.2f}**\n\n"
    )

    if z > 2:
        msg += "🚨 **治安悪化の原因です（上位2%の民度）**"
    elif z > 1:
        msg += "⚠ **少し口が悪い傾向があります**"
    elif z < -1:
        msg += "😇 **むしろ治安を良くしている側です**"
    else:
        msg += "🙂 **普通レベルです**"

    await interaction.response.send_message(msg)

client.run(TOKEN)




