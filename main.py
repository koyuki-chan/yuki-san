from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import asyncio
from cogs.bili_api import get_info_live,get_info
import datetime



#config zone 配置區
load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = discord.Bot()
bot.load_extension('cogs.commands')
bot.load_extension('cogs.live')
bot.load_extension('cogs.dyn')

bot.run(TOKEN)
