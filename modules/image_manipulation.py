from imports import *

def wrap(font, text, line_width):
    words = text.split()
    lines = []
    line = []
    for word in words:
        newline = ' '.join(line + [word])
        w,h = font.getsize(newline)
        if w > line_width:
            lines.append(' '.join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(' '.join(line))
    return '\n'.join(lines)

def add_corners(im, rad=10):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, "white")
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def ReduceOpacity(img, opacity):
    assert opacity >= 0 and opacity <= 1
    img = img.copy()
    x = img.split()[3]
    x = ImageEnhance.Brightness(x)
    x = x.enhance(opacity)
    img.putalpha(x)
    return img

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

class ImageManipulation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deepfry(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                return await usage(ctx, ['mention a user'], [ctx.author.mention], "Deepfries a user's avatar.")
            emoji = 0
            z = (300,300)
            ok = Image.open("assets/ok.png")
            lol = Image.open("assets/lol.png")
            noise = Image.open("assets/noise.jpg")

            img = requests.get(user.avatar_url)
            img = BytesIO(img.content)
            img = Image.open(img)
            img = img.resize((800,800))
            base = img.convert('RGBA')
            noise = noise.resize((800,800)).convert('RGBA')
            if emoji is 1:

                ok = ok.resize(z)
                lol = lol.resize(z).convert('RGBA')
                ok = ok.rotate(30)
                lol = lol.rotate(40)

                base.paste(ok, (521,240), ok)
                base.paste(lol, (75,70), lol)

            img = Image.blend(base, noise, .2)
            img = ImageEnhance.Color(img)
            img = img.enhance(4.0)
            img = change_contrast(img, 200)
            file = BytesIO()
            img.save(file, "png")
            file.seek(0)
            await ctx.send(file=discord.File(file, 'meme.png'))
        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def spiderglasses(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        try:
            if user2 is None:
                user2 = ctx.author
            if user1 is None:
                return await usage(ctx, ['mention a user', 'mention the second user'], [ctx.author.mention, ctx.me.mention], 'Puts the two user\'s avatar in a spiderman glasses meme.')

            size = (210, 210)
            base = Image.open("assets/spiderglasses.jpg")

            u1 = requests.get(user1.avatar_url)
            u2 = requests.get(user2.avatar_url)

            url1 = BytesIO(u1.content)
            url1 = Image.open(url1).resize(size).convert('RGBA')
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)

            url2 = BytesIO(u2.content)
            url2 = Image.open(url2).resize(size).convert('RGBA')

            base.paste(url1, (279,18), url1)
            base.paste(url2, (279,283), url2)
            file = BytesIO()
            base.save(file, "png")
            file.seek(0)
            await ctx.send(file=discord.File(file, 'gay.png'))

        except Exception as e:
            await botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(ImageManipulation(bot))
