from discord.ext import commands
from tools import utils

class GeneralCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        try:
            pass
        except Exception as e:
            await utils.botError(self.bot, ctx, e)

    @commands.command()
    async def ping(self, ctx):
        try:
            pong = round(self.bot.latency*1000)
            await ctx.sends(f":ping_pong: Hey, My latency is `{pong}ms`. Now that is epic.")
        except Exception as e:
            await utils.botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))
