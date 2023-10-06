import discord
from discord.ext import commands
import config
import sys
import requests
from lets_common_log import logUtils as log
from last_meal_info import last_meal

conf = config.config("config.ini")
if not conf.checkConfig():
    conf.generateDefaultConfig()
    sys.exit("config.ini 재설정")
HOST = conf.config["server"]["host"]
PORT = conf.config["server"]["port"]
discord_token = conf.config["discord"]["token"]

# 봇 객체 생성
bot = commands.Bot(command_prefix='!')  # 봇의 명령 접두사를 설정합니다.

# 봇이 로그인할 때 실행되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# !hello 명령어에 대한 이벤트 핸들러
@bot.command(aliases=["핑"])
async def ping(ctx):
    await ctx.send('pong!')

@bot.command(aliases=["급식"])
async def meal(ctx):
    r = requests.get(f"http://localhost:{PORT}", headers={"User-Agent": "meal discord"})
    r = r.json()

    log.info(f"r = {r}")

    if type(r) == list:
        msg = ""
        for i in r:
            msg += i + "\n"
    elif type(r) == dict:
        LMI = last_meal()
        msg = \
            str(r) +\
            "\n\n\n" +\
            "제작자의 말 : `'CODE': 'INFO-200'` 이면, 나이스 API에서 성포고 급식이 누락됨" +\
            "\n\n\n" +\
            "**마지막 급식 정보**\n" + \
            f"급식일:{LMI['last_date']} | 업데이트일:{LMI['last_update']}\n" + \
            f"{LMI['last_meal']}"

    embed = discord.Embed(title='오늘의 급식', description=msg, url=f'http://localhost:{PORT}/', color=discord.Color.random())
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_author(name=bot.user.name, url="https://discord.com/users/753682115505160393", icon_url=bot.user.avatar_url)
    # Timestamp 설정 (현재 시간 사용)
    embed.timestamp = ctx.message.created_at
    embed.set_footer(text="Made by aodd.xyz", icon_url="https://collabo.lol/img/setFooter.webp")
    await ctx.send(embed=embed)

# 봇 실행
if __name__ == '__main__':
    # 봇의 토큰을 여기에 입력하세요.
    bot.run(discord_token)