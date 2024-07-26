
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import asyncio
import datetime



#config zone 
load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = discord.Bot()
bot.load_extension('cogs.commands')
bot.load_extension('cogs.link')
# bot.load_extension('cogs.live')
bot.load_extension('cogs.dyn')

bot.run(TOKEN)