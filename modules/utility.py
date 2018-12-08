from imports import *

class Utilities:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def memes_count(self, ctx):
        try:
            amount = db.memes.count({})
            e = discord.Embed(title="Woah that's a lot of memes", description=f"There are currently {amount} memes in the database. You can help increase this number by uploading memes using the `{prefix(ctx)}upload_meme` command.", color=color())
            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            await ctx.send(embed=e)
        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def profiles_count(self, ctx):
        try:
            amount = db.profiles.count({})
            since_restart = Counters.profiles_since_restart
            e = discord.Embed(title="Profiles Counter", description=f"""
Total amount of profiles in the database : {amount}
Total amount of profiles created since restart : {since_restart}
""", color=color())
            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            await ctx.send(embed=e)
        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def messages_sent(self, ctx):
        try:
            x = len(Counters.messages_sent)
            s = "s"
            if x < 2:
                s = ""
            e = discord.Embed(title="Messages sent since restart", description=f"{x} message{s}.", color=color())
            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            await ctx.send(embed=e)
        except Exception as e:
            await botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(Utilities(bot))
