#-- coding: utf-8 --
import discord
from discord.ext import commands
import asyncio
from cogs import bili_api # type: ignore
import datetime
import os, json
from bilibili_api import sync, exceptions

class BilibiliDyncNotifier(commands.Cog):
    def __init__(self, bot, uid, channel_id):
        self.bot = bot
        self.uid = uid
        self.channel_id = channel_id
        self.timestamp = 0
        self.loop = asyncio.get_event_loop()
        
    async def notify_dynamic(self, data):
        channel = self.bot.get_channel(self.channel_id)
        name = data['user_profile']['info']['uname']
        dynamic_id = data['dynamic_id']
        embed = discord.Embed(title=f'', description=f'{name} 發佈了一則新的動態.\nhttps://t.bilibili.com/{dynamic_id}', color=0x03b2f8)
        embed.set_author(name=name, url=f'https://space.bilibili.com/{self.uid}', icon_url=data['user_profile']['info']['face'])
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        
    async def check_dynamic(self):
        try:
            data = await bili_api.fetch_dyn()
            if self.timestamp == 0:
                self.timestamp = data['timestamp']
                
            elif self.timestamp < data['timestamp']:
                await self.notify_dynamic(data)
                self.timestamp = data['timestamp']
        except exceptions.NetworkException as e:
            if e.status == 429:
                print("Too many requests, waiting before retrying...")
                await asyncio.sleep(300)  # 等待 5 分鐘後重試
            else:
                print(f"NetworkException occurred: {e.status} - {e.message}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    @commands.Cog.listener()
    async def on_ready(self):
        print("Tracking user dynamic...")
        while True:
            try:
                await self.check_dynamic()
            except Exception as e:
                print(f"Error in loop: {e}")
            await asyncio.sleep(120)
        
    async def close(self):
        # 在事件循環關閉前進行清理
        print("Cleaning up before closing event loop...")
        await asyncio.sleep(1)

def setup(bot):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    parent_dir = os.path.join(parent_dir, "config.json")
    with open(parent_dir, "r") as file:
        json_data = json.load(file)
    
    uid = json_data['uid']
    channel_id = json_data['channel_ID']
    cog = BilibiliDyncNotifier(bot, uid, channel_id)
    bot.add_cog(cog)
    
    # 添加在機器人關閉時執行的清理操作
    bot.loop.run_until_complete(cog.close())
