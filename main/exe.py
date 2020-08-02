import discord
import time
import datetime
from bs4 import BeautifulSoup
from urllib import request
import wikipedia
import secret

client = discord.Client()


# online message
@client.event
async def on_ready():
    print("Its ok")


# receive message
@client.event
async def on_message(message):
    messageArgs = message.content.split()
    # Bot
    if message.author.bot:
        return

    # help
    if messageArgs[0] == "/help":
        await message.channel.send(""
                                   "> **Polacreth**\n"
                                   "> -----------------\n"
                                   "> usage:\n"
                                   ">   /date ... 現在の日時を表示\n"
                                   ">   /atnext ... AtCoderの次回コンテスト予定を表示\n"
                                   "> -----------------\n"
                                   "> updated on 2020/07/31\n"
                                   "> by 48clovA\n"
                                   "")

    # return date
    if messageArgs[0] == "/date":
        await message.channel.send(datetime.datetime.now())

    # return AtCoder next time
    if messageArgs[0] == "/atnext":
        html = request.urlopen("https://atcoder.jp/contests/?lang=ja")
        time.sleep(1)
        soup = BeautifulSoup(html)

        # get next time
        tdList = soup.find(id="contest-table-upcoming").find_all("td")
        nextTime = tdList[0].find("time").text
        contestName = tdList[1].find("a").text
        timeRequired = tdList[2].text
        rated = tdList[3].text

        await message.channel.send(
            f"```xml\nTime : {nextTime.split('+')[0]}\nContest : {contestName}\nTime Required : {timeRequired}\nRated : {rated}\n```")

    # wiki research sys
    if messageArgs[0] == "/wiki":
        # help for wiki
        if len(messageArgs) == 1:
            await message.channel.send("usage: /wiki [調べたい単語]")
            return

        # 言語設定
        wikipedia.set_lang("ja")
        searchResponse = wikipedia.search(messageArgs[1])
        if not searchResponse:
            await message.channel.send("検索結果が見つかりませんでした。キーワードを変更してください")
            return

        try:
            result = wikipedia.summary(messageArgs[1], sentences=3)
            page = wikipedia.page(messageArgs[1])
            resultUrl = page.url
            await message.channel.send(f"Results:\n"
                                       "```\n"
                                       f"{result}\n"
                                       f"```\n"
                                       f"\n"
                                       f"{resultUrl}")

        except wikipedia.exceptions.DisambiguationError as e:
            await message.channel.send("キーワードが抽象的であるため、検索結果を絞ることができませんでした。\n"
                                       "キーワードを変更してください。")


client.run(secret.TOKEN)
