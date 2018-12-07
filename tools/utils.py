import traceback, discord
import datetime, random
from tools.bot_tools import db
from lxml.html import fromstring
import requests


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
{'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'},
{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0'},
{'User-Agent': 'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00'},
{'User-Agent': 'Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50'},
{'User-Agent': 'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02'},
{'User-Agent': 'Opera/9.80 (Android 2.3.3; Linux; Opera Mobi/ADR-1111101157; U; es-ES) Presto/2.9.201 Version/11.50'},
{'User-Agent': 'Opera/9.80 (S60; SymbOS; Opera Mobi/SYB-1107071606; U; en) Presto/2.8.149 Version/11.10'},
{'User-Agent': 'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'},
{'User-Agent': 'Opera/9.80 (Android 2.2.1; Linux; Opera Mobi/ADR-1107051709; U; pl) Presto/2.8.149 Version/11.10'},
{'User-Agent': 'Opera/9.80 (S60; SymbOS; Opera Mobi/SYB-1104061449; U; da) Presto/2.7.81 Version/11.00'},
{'User-Agent': 'Opera/9.80 (S60; SymbOS; Opera Mobi/SYB-1103211396; U; es-LA) Presto/2.7.81 Version/11.00'},
{'User-Agent': 'Opera/9.80 (Android; Linux; Opera Mobi/ADR-1012221546; U; pl) Presto/2.7.60 Version/10.5'},
{'User-Agent': 'Opera/9.80 (Android 2.2;;; Linux; Opera Mobi/ADR-1012291359; U; en) Presto/2.7.60 Version/10.5'},
{'User-Agent': 'Opera/9.80 (Android 2.2; Opera Mobi/ADR-2093533608; U; pl) Presto/2.7.60 Version/10.5'},
{'User-Agent': 'Opera/9.80 (Android 2.2; Opera Mobi/-2118645896; U; pl) Presto/2.7.60 Version/10.5'},
{'User-Agent': 'Opera/9.80 (Android 2.2; Linux; Opera Mobi/ADR-2093533312; U; pl) Presto/2.7.60 Version/10.5'},
{'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'},
{'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'},
{'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9'}
]

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies

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

# the following function was cloned (Had to clone it cause i have no idea how to fix the issue i'm having, it has something to do with imports)

async def giveAchievement(user, id, extra=None):
    if extra is None:
        extra = ""

    # if not db.achievements.count({"id":id}):
        # raise AchievementNotFound('Sorry mate but that achievement is not found. hehehe gaddem')
#
    # if not db.profiles.count({"user_id":user.id}):
        # raise UserNotFound('How sad :(')

    achievements = [x['achievements'] for x in db.profiles.find({"user_id":user.id})][0]

    if id in achievements:
        return

    #if not id in achievements:
    db.profiles.update_one({"user_id":user.id}, {'$push':{'achievements':id}})

    for x in db.achievements.find({"id":id}):
        reward = f"<:gold:514791023671509003> {x['coins']} Coins\n<:diagay:515536803407593486> {x['diamonds']} Diamonds"
        e = discord.Embed(title=f"Wow New Achievement! Such cool", description=f":clap: Congratulations {user.name} you just obtained the achievement {x['name']} {extra}. :clap:\n\nOh and here are your rewards\n{reward}", color=color())
        e.set_thumbnail(url=gif['clap1'])
        footer(user, e)
        await user.send(embed=e)
        db.profiles.update_one({"user_id":user.id}, {'$inc':{'coins':x['coins'], 'diamonds':x['diamonds']}})

async def botError(bot, message, e):
    e = traceback.format_exc()
    em = discord.Embed(title="Oh well an unexpected error has occured", description=f"```{e}```\nThe error has now been sent to the bot developer. (Thank goodness)", color=r)
    em.set_thumbnail(url=gif['disappointed1'])
    footer(message, em)
    await giveAchievement(message.author, 4, extra="for finding an error. Thank you captain :)")
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
