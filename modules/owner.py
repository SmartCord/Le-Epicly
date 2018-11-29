from discord.ext import commands
import discord
from tools import utils
from tools.bot_tools import db

class OwnerGay:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def client_edit(self, ctx, *, new_name: str = None):
        try:
            if new_name is None:
                return await utils.usage(ctx, ['new name'], ['you gay men'], 'Lets you change the bot\'s actual name (Not nickname).')

            await self.bot.user.edit(username=new_name)
            await utils.success(ctx, "Successfully changed the name to {}".format(new_name))

        except Exception as e:
            await utils.botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(OwnerGay(bot))
