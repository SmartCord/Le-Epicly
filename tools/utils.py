from pymongo import MongoClient
import traceback, discord
import datetime, random
from os import environ


db_password = environ.get('db_password')
db_uri = "mongodb://zen:{}@leepiclybot-shard-00-00-wrvha.mongodb.net:27017,leepiclybot-shard-00-01-wrvha.mongodb.net:27017,leepiclybot-shard-00-02-wrvha.mongodb.net:27017/test?ssl=true&replicaSet=LeEpiclyBot-shard-0&authSource=admin&retryWrites=true".format(db_password)


c = 0x0a91ff
g = 0x18d45c
r = 0xff4343

client = MongoClient(db_uri)
db = client['epic']

def color():
    return random.choice([0xff66c1, 0x6666c1, 0xb0d996, 0x588585, 0x21ff94, 0x1d4457, 0x77003c, 0x936dd4, 0xd46db6, 0x48cfa6])

def prefix(message):
    if db.server_prefixes.count({"server_id":message.guild.id}):
        return [x['prefix'] for x in db.server_prefixes.find({"server_id":message.guild.id})][0]
    return "?"

def footer(ctx, embed, extra=None):
    try:
        if ctx.author.avatar_url:
            avatar = ctx.author.avatar_url
        else:
            avatar = ctx.me.avatar_url
        author = ctx.author
    except:
        avatar = ctx.avatar_url
        author = ctx
    embed.timestamp = datetime.datetime.utcnow()
    if extra is None:
        extra = ""
    else:
        extra = " " + extra
    embed.set_footer(text=f"{author}{extra}", icon_url=avatar)

async def botError(bot, message, e):
    e = traceback.format_exc()
    em = discord.Embed(title="An unexpected error has occured", description=f"```{e}```\nThe error has now been sent to the bot developer", color=r)
    em.set_thumbnail(url=bot.user.avatar_url)
    footer(message, em)
    await message.send(embed=em)

    if message.author.id == 363880571614527488:
        return

    ctx = bot.get_channel(514437538564538384)
    em = discord.Embed(title=f"Command Error", description=f"Command : {message.message.content}\n \
    User : {message.author} ({message.author.id})\n \
    Server : {message.guild} ({message.guild.id})", color=r)
    em.add_field(name="Error", value=f"```{e}```")
    if message.author.avatar_url:
        a = message.author.avatar_url
    else:
        a = message.me.avatar_url
    em.set_thumbnail(url=a)
    await ctx.send(embed=em)
