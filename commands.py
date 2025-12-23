from enum import Enum
import json
from os import name
from discord import app_commands
import discord

import ai
from shared.db import get_avg_rank, get_avg_userscore, get_server_avg, get_server_stddev

@app_commands.command(name="avg_toxiscore",description="ユーザーの平均暴言スコアを取得します")
async def avg_toxiscore(interaction:discord.Interaction,user:discord.Member = None):
    if(user == None):
        user = interaction.user
    avg_score = get_avg_userscore(user.id,interaction.guild.id)
    if avg_score:
        await interaction.response.send_message(avg_score)
    else:
        await interaction.response.send_message("ユーザーはまだ発言をしていません")

@app_commands.command(
    name="toxicity_rank",
    description="サーバー平均と比較した治安影響スコアを表示します",
)
async def toxicity_rank(interaction: discord.Interaction, user: discord.Member = None):
    await interaction.response.defer(ephemeral=True)
    if user is None:
        user = interaction.user

    guild = interaction.guild
    user_avg = get_avg_userscore(user.id,guild.id)
    server_avg = get_server_avg(guild.id)
    server_std = get_server_stddev(guild.id)

    if user_avg == None or server_avg == None:
        await interaction.followup.send("サーバー平均が存在していないかユーザーはまだ発言していません")
        return

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

    await interaction.followup.send(msg)

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


class rankType(Enum):
    avg = "avg"
    total = "total"

@app_commands.command(
        name="ranking",
        description="サーバーの治安にどのくらい影響を与えているかのランキングを表示します"
)
async def ranking(interaction:discord.Interaction,worst:bool = False,limit:int = 5,min_post:int = 10,type:rankType = rankType.avg):
    if type == rankType.avg:

        rows = get_avg_rank(worst=worst,limit=limit,guild_id=interaction.guild.id,min_post=min_post)
    elif type == rankType.total            :
        rows = ()
    res = ""
    if not worst: 
        res = "サーバーの優良ユーザーランキング"
    else:
        res = "サーバー平均暴言度ランキング"
    count = 1
    for row in rows:
        res += f"\n #{count}  <@{row[0]}>:平均暴言指数{row[1]}"
        count +=1
    await interaction.response.send_message(res,ephemeral=True)


@app_commands.command(
        name="check",
        description = "入力がどのくらいの暴言なのか調べます"
)
async def check(interaction:discord.Interaction,msg:str):
    await interaction.response.defer()
    score = (await ai.judge_message([msg]))[0]
    await interaction.followup.send(f"発言は{score}点です")


def setup(tree: app_commands.CommandTree) -> None:
    tree.add_command(avg_toxiscore)
    tree.add_command(toxicity_rank)
    tree.add_command(add_exclude_channel)
    tree.add_command(remove_exclude_channel)
    tree.add_command(ranking)
    tree.add_command(check)