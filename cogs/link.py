import discord
from discord.ext import commands
import re
from cogs.bili_api import get_dync_info, isOpus
from datetime import datetime

class Sending_link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def send_link(self, ctx, url: discord.Option(str)):
        if not (url.startswith("https://t.bilibili.com/") or url.startswith("https://www.bilibili.com/opus/")):
            await ctx.respond("Invalid URL format")
            return
        
        pattern = r'\d+'
        numbers = re.findall(pattern, url)
        
        if numbers:
            try:
                data = await get_dync_info(int(numbers[0]))
                if isOpus(int(numbers[0])):
                    author = data['item']['modules']['module_author']
                    author_name = author['name']
                    author_avatar = author['face']
                    pub_time_str = author['pub_time']
                    content = data['item']['modules']['module_dynamic']['desc']['text']
                    images=[]
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
                
                pub_time = datetime.strptime(pub_time_str, "%Y年%m月%d日 %H:%M")
                
                
                base_embed = discord.Embed(title="Bilibili Dynamic", description=content, timestamp=pub_time)
                base_embed.set_author(name=author_name, icon_url=author_avatar)
                base_embed.set_footer(text="From Bilibili")
                embed = base_embed.copy() 
                embeds = [embed]
                for image in images:
                    embed = discord.Embed()
                    embed.set_image(url=image)
                    embeds.append(embed)
                
                # Send all embeds
                await ctx.respond(embeds=embeds)

            except Exception as e:
                await ctx.respond("Invalid URL")
                print(f"error:{e}")
        else:
            await ctx.respond("Invalid URL")


def setup(bot):
    bot.add_cog(Sending_link(bot))