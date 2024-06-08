#-- coding: utf-8 --
import discord
from discord.ext import commands
import asyncio
from cogs import bili_api # type: ignore
import datetime
import os, json

class BilibiliIconNotifier(commands.Cog):
    def __init__(self,bot,uid,channel_id,url):
        self.bot = bot
        self.uid = uid
        self.channel_id = channel_id
        self.icon_url = url
        self.loop = asyncio.get_event_loop()
        
    async def notify_icon_change(self,url):
        
        channel = self.bot.get_channel(self.channel_id)
        name = self.info[self.uid]['name']
        embed = discord.Embed(title=f'', description=f'{name} has changed his/her avatar.', color=0x03b2f8)
        embed.set_author(name=name, url=f'https://space.bilibili.com/{self.uid}', icon_url=url)
        embed.set_image(url=url)
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        
    async def check_icon_change(self):
        i = bili_api.get_info(self.uid)
        self.info = i
        icon = i[self.uid]['icon']
        if icon != self.icon_url:
            await self.notify_icon_change(icon)
            self.icon_url = icon
            
    @commands.Cog.listener()
    async def on_ready(self):
        # print(f"{self.bot.user} is ready and online!")
        print("Traking avator...")
        while True:
            await self.check_icon_change()
            await asyncio.sleep(60)
        
def setup(bot):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    parent_dir = os.path.join(parent_dir,"config.json")
    with open(parent_dir,"r") as file:
        json_data = json.load(file)
    
    uid = json_data['uid']
    channel_id = json_data['channel_ID']
    t = bili_api.get_info(uid)
    icon_url = t[uid]['icon']
    bot.add_cog(BilibiliIconNotifier(bot,uid,channel_id,icon_url))