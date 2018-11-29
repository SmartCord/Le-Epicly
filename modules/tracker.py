from imports import *

class Tracker:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        try:
            labels = ['Test Gay', 'Test Gay Again']
            values = [3824, 1392]

            trace = go.Pie(labels=labels, values=values)
            file = BytesIO()
            pio.write_image([trace], file)
            file.seek(0)
            await ctx.send(file=discord.File(file, 'test.png'))

        except Exception as e:
            await botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(Tracker(bot))
