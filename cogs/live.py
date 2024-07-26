#-- coding: utf-8 --
import discord
from discord.ext import commands
import asyncio
from cogs import bili_api # type: ignore
from cogs.config import config 
import datetime
import os,json
from bilibili_api import sync, exceptions

class BilibiliLiveNotifier(commands.Cog):
    def __init__(self, bot, uid, channel_id):
        self.bot = bot
        self.uid = uid
        self.channel_id = channel_id
        self.live_status = None
        self.data ={}
        self.loop = asyncio.get_event_loop()

    async def notify_live_start(self):
        channel = self.bot.get_channel(self.channel_id)
        name = self.data['name']
        title = self.data['live_room']['title']
        url = self.data['live_room']['url']
        embed = discord.Embed(title=title, description=f'{name} is streaming.', color=0x03b2f8,url=url)
        embed.set_author(name=name, url=f'https://space.bilibili.com/{self.uid}', icon_url=self.data['face'])
        embed.set_image(url=self.data['live_room']['cover'])
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)

    async def check_live_status(self):
        try:
            data = await bili_api.get_info_live()
            self.data = data
            if data['live_room']['liveStatus'] == 1 and self.live_status != 1:
                self.live_status = 1
                await self.notify_live_start()
            else:
                self.live_status = int( data['live_room']['liveStatus'] )
        except exceptions.NetworkException as e:
            if e.status == 429:
                print("Too many requests, waiting before retrying...")
                await asyncio.sleep(300)
                  
        except Exception as e:
            print(f"Am error occurred: {e}")
            await asyncio.sleep(300)            
    
    @commands.Cog.listener()
    async def on_ready(self):
        # print(f"{self.bot.user} is ready and online!")
        print("Traking...")
        while True:
            try:
                await self.check_live_status()
            except Exception as e:
                print(f"Error in loop: {e}")
            await asyncio.sleep(120)
    
    async def close(self):
        # 在事件循環關閉前進行清理
        print("Cleaning up before closing event loop...")
        await asyncio.sleep(1)        

def setup(bot):
    uid =  config.UID
    channel_id = config.CHANNEL_ID
    cog = BilibiliLiveNotifier(bot, uid,channel_id)
    bot.add_cog(cog)
    bot.loop.run_until_complete(cog.close())