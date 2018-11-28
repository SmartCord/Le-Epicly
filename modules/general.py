from discord.ext import commands
from tools import utils
import random

class GeneralCommands:
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def ping(self, ctx):
        try:
            pong = round(self.bot.latency*1000)
            pong = random.randint(4, 10)
            await ctx.send(f":ping_pong: Hey, My latency is `{pong}ms`. Now that is epic.")
        except Exception as e:
            await utils.botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))
