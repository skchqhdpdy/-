import discord
from discord.ext import commands
from flask import Flask
import asyncio
import config
import sys

conf = config.config("config.ini")
if not conf.checkConfig():
    conf.generateDefaultConfig()
    sys.exit("config.ini 재설정")
discord_token = conf.config["discord"]["token"]

# Discord.py 봇
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def ping(ctx):
    await ctx.send("Hello, I'm your Discord bot!")

# Flask 웹 서버
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! This is a Flask web server.'

# 비동기 이벤트 루프 시작
async def start_bot():
    await bot.start(discord_token)

# 비동기 이벤트 루프 실행
loop = asyncio.get_event_loop()
loop.create_task(start_bot())

if __name__ == '__main__':
    app.run()
