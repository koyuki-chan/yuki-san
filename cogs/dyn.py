
#-- coding: utf-8 --
import discord
from discord.ext import commands
import asyncio
from cogs import bili_api
from cogs.config import config 
from datetime import datetime
from bilibili_api import exceptions

class BilibiliDyncNotifier(commands.Cog):
    def __init__(self, bot, uid, channel_id):
        self.bot = bot
        self.uid = uid
        self.channel_id = channel_id
        self.timestamp = 0
        self.loop = asyncio.get_event_loop()
        
    async def notify_dynamic(self, data):
        channel = self.bot.get_channel(self.channel_id)
        dynamic_id = data['dynamic_id']
        try:
            data = await bili_api.get_dync_info(int(dynamic_id))
            if bili_api.isOpus(int(dynamic_id)):
                author = data['item']['modules']['module_author']
                author_name = author['name']
                author_avatar = author['face']
                pub_time_str = author['pub_time']
                content = data['item']['modules']['module_dynamic']['desc']['text']
                images = []
                major_module = data['item']['orig']['modules']['module_dynamic'].get('major', {})
                opus = major_module.get('opus', {})
                if opus:
                    for pic in opus.get('pics', []):
                        images.append(pic.get('url', ''))
            else:
                author_info = data['item']['modules']['module_author']
                dynamic_info = data['item']['modules']['module_dynamic']['major']['opus']
                author_name = author_info['name']
                author_avatar = author_info['face']
                pub_time_str = author_info['pub_time']
                content = dynamic_info['summary']['text']
                images = [pic['url'] for pic in dynamic_info['pics']]

            #change str time format    
            pub_time = datetime.strptime(pub_time_str, "%Y年%m月%d日 %H:%M")  
            base_embed = discord.Embed(title=f"{author_name} has posted a new dynamic please check. https://t.bilibili.com/{dynamic_id}", description=content, timestamp=pub_time,color=0x03b2f8)
            base_embed.set_author(name=author_name,url=f'https://space.bilibili.com/{self.uid}', icon_url=author_avatar)
            base_embed.set_footer(text="From Bilibili")
            embed = base_embed.copy() 
            
            embeds = [embed]
            if images:
                for image in images:
                   embed = discord.Embed()
                   embed.set_image(url=image)
                   embeds.append(embed)
            # Send all embeds
            await channel.send(embeds=embeds)

        except Exception as e:
            print(e)
        
    async def check_dynamic(self):
        try:
            data = await bili_api.fetch_dyn()
            if self.timestamp == 0:
                self.timestamp = data['timestamp']
                
            elif self.timestamp < data['timestamp']:
                await self.notify_dynamic(data)  # if update send embed messages
                self.timestamp = data['timestamp']
        except exceptions.NetworkException as e:
            if e.status == 429:
                print("Too many requests, waiting before retrying...")
                await asyncio.sleep(300)  # if error wait for 5 mins
            else:
                print(f"NetworkException occurred: {e.status} - {e.message}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    @commands.Cog.listener()
    async def on_ready(self):
        print("Tracking user dynamic...")
        print("Traking user",self.uid)
        while True:
            try:
                await self.check_dynamic()
            except Exception as e:
                print(f"Error in loop: {e}")
            await asyncio.sleep(120) # 2 mins refresh
        
    async def close(self):
        print("Cleaning up before closing event loop...")
        await asyncio.sleep(1)

def setup(bot):
    uid = config.UID
    channel_id = config.CHANNEL_ID
    cog = BilibiliDyncNotifier(bot, uid, channel_id)
    bot.add_cog(cog)
    
    bot.loop.run_until_complete(cog.close())