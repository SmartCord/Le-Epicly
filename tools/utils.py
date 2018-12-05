import traceback, discord
import datetime, random
from tools.bot_tools import db

default_prefix = "?"
c = 0x0a91ff
g = 0x18d45c
r = 0xff4343

gif = {
    'no1':'https://media.giphy.com/media/6Q2KA5ly49368/giphy.gif',
    'disappointed1':'https://media.giphy.com/media/U4VXRfcY3zxTi/giphy.gif',
    'clap1':'https://media.tenor.com/images/96952c4cc0d24d6bb341adefc0932814/tenor.gif',
    'hmm1':'https://media0.giphy.com/media/y3QOvy7xxMwKI/giphy.gif',
    'enough1':'https://media.giphy.com/media/3oEduKiu3xvjkYvCww/200.gif'
}

user_agents = [
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'},
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'},
{'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36'},
{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'},
{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'},
{'User-Agent': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'},
{'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16'},
{'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'}
]

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def color():
    return random.choice([0x1bb596, 0x1ce1b9, 0x65f0d4, 0x68b5a6])

def prefix(message):
    try:
        if db.server_prefixes.count({"server_id":message.guild.id}):
            return [x['prefix'] for x in db.server_prefixes.find({"server_id":message.guild.id})][0]
        return default_prefix
    except:
        return default_prefix

def guildIcon(ctx, guild):
    try:
        return guild.icon_url if guild.icon_url != "" else ctx.me.avatar_url
    except:
        try:
            return ctx.me.avatar_url
        except:
            try:
                return ctx.author.avatar_url
            except:
                return None

async def usage(ctx, arguments, example, description):
    prefixx = prefix(ctx)
    args = [f"<{arg}>" for arg in arguments]
    arguments = " ".join(args)
    example = " ".join(example)
    command = ctx.command.qualified_name
    e = discord.Embed(title="Wrong Usage", color=color())
    e.add_field(name="Proper Usage", value=f"{prefixx}{command} {arguments}")
    e.add_field(name="\u200b", value="\u200b")
    e.add_field(name="Example", value=f"{prefixx}{command} {example}")
    e.add_field(name="Description", value=description)
    e.set_thumbnail(url=gif['no1'])
    footer(ctx, e)
    await ctx.send(embed=e)

async def error(ctx, error, description):
    e = discord.Embed(title=error, description=description, color=r)
    e.set_thumbnail(url=ctx.me.avatar_url)
    footer(ctx, e)
    await ctx.send(embed=e)

async def success(ctx, message, image=None):
    e = discord.Embed(title="Success!", description=message, color=g)
    try:
        e.set_thumbnail(url=ctx.avatar_url) if not image else None
    except:
        e.set_thumbnail(url=ctx.author.avatar_url) if not image else None
    e.set_image(url=image) if image else None
    footer(ctx, e)
    await ctx.send(embed=e)

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
    em = discord.Embed(title="Oh well an unexpected error has occured", description=f"```{e}```\nThe error has now been sent to the bot developer. (Thank goodness)", color=r)
    em.set_thumbnail(url=gif['disappointed1'])
    footer(message, em)
    await message.send(embed=em)

    if message.author.id == 363880571614527488: # Your ID
        return

    ctx = bot.get_channel(517276933344460820) # Channel to send message
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
