
import discord
import os
import aiohttp
import json
import hashlib
from discord.ext import commands
import aiofiles
# 經驗值需求表
exp_table = {
    1: 15, 2: 30, 3: 30, 4: 35, 5: 35, 6: 35, 7: 40, 8: 40, 9: 40, 10: 60,
    11: 90, 12: 105, 13: 120, 14: 140, 15: 160, 16: 180, 17: 205, 18: 230, 19: 255, 20: 285,
    21: 315, 22: 345, 23: 375, 24: 410, 25: 445, 26: 480, 27: 520, 28: 560, 29: 600, 30: 645,
    31: 690, 32: 735, 33: 780, 34: 830, 35: 880, 36: 930, 37: 985, 38: 1040, 39: 1095, 40: 1155,
    41: 1215, 42: 1275, 43: 1335, 44: 1400, 45: 1465, 46: 1530, 47: 1600, 48: 1670, 49: 1740
}

# 累計經驗值表
cumulative_exp = {
    1: 0, 2: 15, 3: 45, 4: 75, 5: 110, 6: 145, 7: 180, 8: 220, 9: 260, 10: 300,
    11: 360, 12: 450, 13: 555, 14: 675, 15: 815, 16: 975, 17: 1155, 18: 1360, 19: 1590, 20: 1845,
    21: 2130, 22: 2445, 23: 2790, 24: 3165, 25: 3575, 26: 4020, 27: 4500, 28: 5020, 29: 5580, 30: 6180,
    31: 6825, 32: 7515, 33: 8250, 34: 9030, 35: 9860, 36: 10740, 37: 11670, 38: 12655, 39: 13695, 40: 14790,
    41: 15945, 42: 17160, 43: 18435, 44: 19770, 45: 21170, 46: 22635, 47: 24165, 48: 25765, 49: 27435, 50: 29175
}


class Greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_hash_code(self, key, path):
        async with aiofiles.open('cogs/url.json', 'r', encoding='utf-8') as f:
            data = json.loads(await f.read())
        
        url = data['key'][key]['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as pic_res:
                if pic_res.status == 200:
                    data = await pic_res.json()
                    source_hash = data["data"][0]["hash"]
                else:
                    print(f"Error: {pic_res.status} - {pic_res.text}")
                    return False

        async with aiofiles.open(path, 'rb') as f:
            img_data = await f.read()
            img_hash = hashlib.md5(img_data).hexdigest()

        return img_hash == source_hash
                
    async def download_pic(self, key):
        async with aiofiles.open('cogs/url.json', 'r', encoding='utf-8') as f:
            data = json.loads(await f.read())
        
        url = data['key'][key]['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = f'https://arona.cdn.diyigemt.com/image{data["data"][0]["content"]}'
                else:
                    print(f"Error: {response.status} - {response.text}")
                    return

            async with session.get(img_url) as pic_response:
                if pic_response.status == 200:
                    if key == "future_pool":
                        file_path = f'./data/{key}/国际服未来视.png'
                    elif key == "grand_assault":
                        file_path = f'./data/{key}/国际服大决战.png'
                    elif key == "total_assault":
                        file_path = f'./data/{key}/国际服总力.png'
                    elif key == "current_event":
                        file_path = f'./data/{key}/国际服活动.png'
                    elif key == "joint_firing_drill":
                        file_path = f'./data/{key}/国际服火力演习.png'
                    
                    async with aiofiles.open(file_path, 'wb') as f1:
                        await f1.write(await pic_response.read())
                    print(f"Image downloaded and saved to: {file_path}")
                else:
                    print(f"Failed to download image. Status code: {pic_response.status}")

    @discord.slash_command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        await ctx.respond(f"Latency is {self.bot.latency:.2f}s")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is ready and online!")

    @discord.slash_command()
    async def future_pool(self, ctx):
        img_path = 'data/future_pool/国际服未来视.png'

        await ctx.defer()

        if not os.path.exists(img_path):
            print("Downloading the picture...")
            await self.download_pic("future_pool")
        else:
            if not await self.check_hash_code("future_pool", img_path):
                print("Updating the latest pic...")
                await self.download_pic("future_pool")
             
        await ctx.followup.send(file=discord.File(img_path))
        
    @discord.slash_command()
    async def grand_assault(self, ctx):
        img_path = 'data/grand_assault/国际服大决战.png'

        await ctx.defer()

        if not os.path.exists(img_path):
            print("Downloading the picture...")
            await self.download_pic("grand_assault")
        else:
            if not await self.check_hash_code("grand_assault", img_path):
                print("Updating the latest pic...")
                await self.download_pic("grand_assault")
             
        await ctx.followup.send(file=discord.File(img_path))
        
    @discord.slash_command()
    async def total_assault(self, ctx):
        img_path = 'data/total_assault/国际服总力.png'

        await ctx.defer()

        if not os.path.exists(img_path):
            print("Downloading the picture...")
            await self.download_pic("total_assault")
        else:
            if not await self.check_hash_code("total_assault", img_path):
                print("Updating the latest pic...")
                await self.download_pic("total_assault")
             
        await ctx.followup.send(file=discord.File(img_path))       

    @discord.slash_command()
    async def current_event(self, ctx):
        img_path = 'data/current_event/国际服活动.png'

        await ctx.defer()

        if not os.path.exists(img_path):
            print("Downloading the picture...")
            await self.download_pic("current_event")
        else:
            if not await self.check_hash_code("current_event", img_path):
                print("Updating the latest pic...")
                await self.download_pic("current_event")
             
        await ctx.followup.send(file=discord.File(img_path))
    
    @discord.slash_command()
    async def joint_firing_drill(self,ctx):
        img_path = 'data/joint_firing_drill/国际服火力演习.png'
        await ctx.defer()
        if not os.path.exists(img_path):
            print("Downloading the joint firing drill pic...")
            await self.download_pic("joint_firing_drill")
        else:
            if not await self.check_hash_code("joint_firing_drill",img_path):
                print("Updating the latest pic...")
                await self.download_pic("joint_firing_drill")

        await ctx.followup.send(file=discord.File(img_path))

    @discord.slash_command()
    async def help(self,ctx):
        embed = discord.Embed(title="HELP",description="所有攻略都是關於蔚藍檔案國際服的，可能會因爲AronaBot未更新圖庫導致傳送了過去的攻略，另外由於是直接傳送圖片，回應速度會偏慢。\n\n/future_pool 會發送**國際服的未來視** 注意可能會有拆包情報的卡池在內 \n\n/grand_assault 會發送關於**大決戰**的攻略\n\n/total_assault 會發送關於**總力戰**的攻略\n\n/current_event 會發送當下**活動**的攻略\n\n/joint_firing_drill 會發送**戰術火力**的攻略",color=0x03b2f8)
        await ctx.respond(embed=embed)

    @discord.slash_command()
    async def calculate_affection(self,ctx,current: discord.Option(int),target: discord.Option(int)):
        if current<1 or target > 50 or  current >= target:
            await ctx.respond("Invalid value")
        else:
            current_exp = cumulative_exp[current]
            target_exp = cumulative_exp[target]
            need = target_exp - current_exp
            gifts_needs =  need / 60
            embed = discord.Embed(title="BA羈絆計算器",description=f"目前羈絆等級為 ***{current}***，目標等級為 ***{target}***，\n距離目標還差 ***{need}*** 經驗，大概還需要 ***{gifts_needs}*** 個60羈絆EXP禮物。")
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Greeting(bot))
