import discord
from discord.ext import commands
import config
import sys

conf = config.config("config.ini")
if not conf.checkConfig():
    conf.generateDefaultConfig()
    sys.exit("config.ini 재설정")
discord_token = conf.config["discord"]["token"]

# 봇 객체 생성
bot = commands.Bot(command_prefix='!')  # 봇의 명령 접두사를 설정합니다.

# 봇이 로그인할 때 실행되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# !hello 명령어에 대한 이벤트 핸들러
@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

# 봇 실행
if __name__ == '__main__':
    # 봇의 토큰을 여기에 입력하세요.
    bot.run(discord_token)