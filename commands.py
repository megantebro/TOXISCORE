import json
from discord import app_commands
import discord

from db import get_avg_userscore, get_server_avg, get_server_stddev

@app_commands.command(name="avg_toxiscore",description="ユーザーの平均暴言スコアを取得します")
async def avg_toxiscore(interaction:discord.Interaction,user:discord.Member = None):
    if(user == None):
        user = interaction.user
    avg_score = get_avg_userscore(user.id)
    await interaction.response.send_message(avg_score)

@app_commands.command(
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

@app_commands.command(
        name="add_exclude_channel",
        description="AIが暴言を検知しなくなるチャンネルを設定します"
)
async def add_exclude_channel(interaction:discord.Interaction,channel:discord.abc.GuildChannel):
    with open("config.json","r") as file:
        json_data = json.load(file)

    json_data["exclude_channel_ids"].append(channel.id)

    with open("config.json","w") as file:
        json_data = json.dump(json_data,file)
    await interaction.response.send_message(channel.jump_url + "を除外リストに追加しました")

@app_commands.command(
        name="remove_exclude_channel",
        description="チェンネルを除外リストから削除します"
)
async def remove_exclude_channel(interaction:discord.Interaction,channel:discord.abc.GuildChannel):
    with open("config.json","r") as file:
        json_data = json.load(file)

    if channel.id not in json_data["exclude_channel_ids"]:
        await interaction.response.send_message(channel.jump_url + "は除外リストにありません")
        return
    
    json_data["exclude_channel_ids"].remove(channel.id)
    with open("config.json","w") as file:
        json.dump(json_data,file)

    await interaction.response.send_message(channel.jump_url + "を除外リストから削除しました")

def setup(tree: app_commands.CommandTree) -> None:
    tree.add_command(avg_toxiscore)
    tree.add_command(toxicity_rank)
    tree.add_command(add_exclude_channel)
    tree.add_command(remove_exclude_channel)