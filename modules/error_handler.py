from imports import *

class SuchError:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.command.qualified_name == "ping":
                e = discord.Embed(title=f"Stop discord bot abuse!", description="Stop pinging the discord bot, you have already used this command 5 times and you have to wait for `{:.2f}` before you can use it again.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                await ctx.send(embed=e)
            else:
                e = discord.Embed(title="Command be cooling down for a moment", description="Sorry but that command is currently on cooldown.\n`{:.2f}s left`.".format(error.retry_after), color=color())
                footer(ctx, e)
                e.set_thumbnail(url=ctx.me.avatar_url)
                await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(SuchError(bot))
