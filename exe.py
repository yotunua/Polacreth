import discord
import time
import datetime
from bs4 import BeautifulSoup
from urllib import request
import secret

client = discord.Client()


# online message
@client.event
async def on_ready():
    print("Its ok")


# receive message
@client.event
async def on_message(message):
    # Bot
    if message.author.bot:
        return

    # help
    if message.content == "/help":
        await message.channel.send(""
                                   "> **Polacreth**\n"
                                   "> -----------------\n"
                                   "> usage:\n"
                                   ">   /date ... 現在の日時を表示\n"
                                   ">   /atnext ... AtCoderの次回コンテスト予定を表示\n"
                                   "> -----------------\n"
                                   "> updated on 2020/07/31\n"
                                   "> by 48clovA\n")

    # return date
    if message.content == "/date":
        await message.channel.send(datetime.datetime.now())

    # return AtCoder next time
    if message.content == "/atnext":
        html = request.urlopen("https://atcoder.jp/contests/?lang=ja")
        time.sleep(1)
        soup = BeautifulSoup(html)

        # get next time
        tdList = soup.find(id="contest-table-upcoming").find_all("td")
        nextTime = tdList[0].find("time").text
        contestName = tdList[1].find("a").text
        timeRequired = tdList[2].text
        rated = tdList[3].text

        await message.channel.send(f"```xml\nTime : {nextTime.split('+')[0]}\nContest : {contestName}\nTime Required : {timeRequired}\nRated : {rated}\n```")


client.run(secret.TOKEN)
