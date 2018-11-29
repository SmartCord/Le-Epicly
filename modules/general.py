from discord.ext import commands
from tools import utils
import random, requests
from io import BytesIO
from PIL import Image
import discord, time

class GeneralCommands:
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def ping(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                previous = time.time()
                pong = round(self.bot.latency*1000)
                pong_edit = pong
                e = discord.Embed(title=":ping_pong: Pongg!", description=f"It took `{pong}ms` to send this message end `{pong_edit}ms` to edit this message.", color=utils.color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                utils.footer(ctx, e)
                first = await ctx.send(embed=e)
                pong_edit = time.time() - previous
                pong_edit = int(round(pong_edit*1000))
                e = discord.Embed(title=":ping_pong: Pongg!", description=f"It took `{pong}ms` to send this message and `{pong_edit}ms` to edit this message.", color=utils.color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                utils.footer(ctx, e)
                await first.edit(embed=e)
                return
            page = requests.get(user.avatar_url)
            page = page.content
            page = BytesIO(page)
            avatar = Image.open(page).resize((320, 320)).convert('RGBA')
            blank = Image.new('RGBA', (256, 256), color=(231, 19, 29))
            tint = Image.open('assets/red.png').convert('RGBA')
            frames = []
            for i in range(8):
                base = blank.copy()

                if i == 0:
                    base.paste(avatar, (-16, -16), avatar)
                else:
                    base.paste(avatar, (-32 + random.randint(-16, 16), -32 + random.randint(-16, 16)), avatar)

                base.paste(tint, (0, 0), tint)

                frames.append(base) # code stolen from dank memer hehheeeh

                # if i == 0:
                    # base.paste(triggered, (-10, 200))
                # else:
                    # base.paste(triggered, (-12 + randint(-8, 8), 200 + randint(0, 12)))


            b = BytesIO()
            frames[0].save(b, save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2,
                           optimize=True)
            b.seek(0)
            await ctx.send(file=discord.File(b, "ping.gif"))
        except Exception as e:
            await utils.botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))
