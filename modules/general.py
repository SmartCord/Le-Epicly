from discord.ext import commands
from tools import utils

class GeneralCommands:
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def help(self, ctx):
        try:
            general = self.bot.get_emoji(515866275503931393)
            utilities = ":gear:"
            image_manipulation = ":camera:"
            e = discord.Embed(title="Bot Help!", description=f"""
Hey there, Welcome to the interactive help menu. Here you can find pages that contains bot commands.
You can use the reactions below to navigate through all categories.

{general} - General Commands
{utilities} - Utiliy Commands
{image_manipulation} - Image Manipulation Commands
""", color=utils.color())
        except Exception as e:
            await utils.botError(self.bot, ctx, e)

    @commands.command()
    async def ping(self, ctx):
        try:
            pong = round(self.bot.latency*1000)
            await ctx.send(f":ping_pong: Hey, My latency is `{pong}ms`. Now that is epic.")
        except Exception as e:
            await utils.botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))
