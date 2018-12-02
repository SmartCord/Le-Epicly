from imports import *

class GeneralCommands:
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def meme(self, ctx):
        try:
            counter = [x['memes'] for x in db.profiles.find({"user_id":ctx.author.id})][0]
            if counter < 1:
                e = discord.Embed(title="Oops no more memes for you", description=f"Sorry but you have used all of your meme points. Luckily all of the memes you have seen has been saved to your meme collection. You can access your meme collection using the `{returnPrefix(ctx)}meme_collection` command.", color=color())
                footer(ctx, e)
                e.set_thumbnail(url=ctx.me.avatar_url)
                await ctx.send(embed=e)
                return

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def points(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                user = ctx.author
            for x in db.profiles.find({"user_id":user.id}):
                is_private = x['is_private']
                if is_private:
                    if user is ctx.author:
                        e = discord.Embed(title="Your profile is private", description="You have decided to set your profile to private. How can you forget about that?", color=color())
                        e.set_thumbnail(url=user.avatar_url)
                        footer(ctx, e)
                        return await ctx.send(embed=e)
                    e = discord.Embed(title="Profile is private", description=f"Sorry but big man {user.name} wants some privacy and has decided to set his profile to be viewed only by him.", color=color())
                    e.set_thumbnail(url=user.avatar_url)
                    footer(ctx, e)
                    return await ctx.send(embed=e)

                memes = x['memes']

            e = discord.Embed(title="Here are all of your points.", color=color())
            e.description = f"""
:small_orange_diamond: Memes : {x['memes']}
"""
            footer(ctx, e)
            await ctx.send(embed=e)

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def store(self, ctx):
        try:
            pg = commands.Paginator(prefix="", suffix="", max_size=1022)
            i = 1
            for x in db.store.find({}):
                line = f"""
{i}. {x['name']}
{x['description']}
<:gold:514791023671509003> Price : {x['coins']} Coins
<:diagay:515536803407593486> Price on diamonds : {x['diamonds']} Diamonds
"""
                i += 1
                pg.add_line(line)


            embeds = []
            for page in pg.pages:
                e = discord.Embed(title="Cool store wow", description=page, color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                embeds.append(e)

            p = paginator.EmbedPages(ctx, embeds=embeds)
            await p.paginate()

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command(aliases=['purchase'])
    async def buy(self, ctx, *, item: str = None):
        try:
            if item is None:
                return await usage(ctx, ['item name'], ['i like memes'], 'Lets you purchase an item from the store.')

            item = item.upper()

            if not db.store.count({"name_upper":item}):
                e = discord.Embed(title="That item doesn't exist", description="Sorry mate but the item you entered doesn't exist. Please make sure the spelling is correct and there are no extra characters.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            e = discord.Embed(title="What do you want to purchase with?", description="Choose by clicking one of the reactions below.", color=color())
            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            embed = await ctx.send(embed=e)
            coin = self.bot.get_emoji(514791023671509003)
            diamond = self.bot.get_emoji(515536803407593486)
            await embed.add_reaction(coin)
            await embed.add_reaction(diamond)

            def check(reaction, user):
                return user == ctx.author

            perks = []

            for x in db.store.find({"name_upper":item}):
                name = x['name']
                coins = x['coins']
                diamonds = x['diamonds']
                try:
                    perks.append(['memes', x['memes']])
                    break
                except:
                    pass

            for x in db.profiles.find({"user_id":ctx.author.id}):
                user_coins = x['coins']
                user_diamonds = x['diamonds']

            if user_coins < 2:
                c = ""
            else:
                c = "s"

            if user_diamonds < 2:
                d = ""
            else:
                d = "s"

            x = False

            for i in perks:
                if 'memes' in i:
                    data = {'$inc':{'memes':i[1]}}

            tries = []

            while x is False:
                if x is False:
                    try:
                        reaction, message = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
                    except asyncio.TimeoutError:
                        return await ctx.send("Timedout")

                if reaction.emoji == coin:
                    if user_coins < coins:
                        e = discord.Embed(title="Not enough coins :(", description=f"You only have {user_coins} Coin{c} and that item costs {coins} Coins.", color=color())
                        e.set_thumbnail(url=ctx.me.avatar_url)
                        footer(ctx, e)

                        if not 1 in tries and len(tries) != 1:
                            e.description += " Try paying with diamonds."
                            tries.append(1)
                        else:
                            if len(tries) >= 1:
                                e.description += " Since you have tried all payment methods with no luck, I have decided to cancel the process for you."
                                return await ctx.send(embed=e)
                        await ctx.send(embed=e)
                    else:
                        db.profiles.update_one({"user_id":ctx.author.id}, data)
                        left = user_coins - coins
                        db.profiles.update_one({"user_id":ctx.author.id}, {'$inc':{"coins":-coins}})
                        if left < 2 and left != 0:
                            lol = f"You now have {left} Coin left."
                        elif left == 0:
                            lol = f"You no longer have any coins. How sad :("
                        else:
                            lol = f"You now have {left} Coins left."

                        message = lol
                        x = True

                elif reaction.emoji == diamond:
                    if user_diamonds < diamonds:
                        e = discord.Embed(title="Not enough diamonds :(", description=f"You only have {user_diamonds} Diamond{d} and that item costs {diamonds} Diamonds.", color=color())
                        e.set_thumbnail(url=ctx.me.avatar_url)
                        footer(ctx, e)
                        if not 2 in tries and len(tries) != 1:
                            e.description += " Try paying with coins."
                            tries.append(2)
                        else:
                            if len(tries) >= 1:
                                e.description += " Since you have tried all payment methods with no luck, I have decided to cancel the process for you."
                                return await ctx.send(embed=e)
                        await ctx.send(embed=e)
                    else:
                        db.profiles.update_one({"user_id":ctx.author.id}, data)
                        left = user_diamonds - diamonds
                        db.profiles.update_one({"user_id":ctx.author.id}, {'$inc':{"diamonds":-diamonds}})
                        if left < 2 and left != 0:
                            lol = f"You now have {left} Diamond left."
                        elif left == 0:
                            lol = f"You no longer have any diamonds. How sad :("
                        else:
                            lol = f"You now have {left} Diamonds left."

                        message = lol
                        x = True
                else:
                    can = await ctx.send("Successfully canceled the process cause you added a different reaction. lel")
                    await embed_msg.delete()
                    await asyncio.sleep(8)
                    await can.delete()
                    return

            await success(ctx, f"Successfully purchased the item `{name}`, {message}")

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def change_privacy(self, ctx, data: str = None):
        try:
            if data is None:
                return await usage(ctx, ['true or false'], ['true'], f"Lets you decide wether you want your profile to be private or not. If this is true then no one else can view your profile.")

            old = [x['is_private'] for x in db.profiles.find({"user_id":ctx.author.id})][0]

            trues = ('YES', 'TRUE', '1')
            noes = ('NO', 'FALSE', '0')
            if data.upper() in trues:
                if old == True:
                    x = "Guess what, your profile is already private. Nothing to change here."
                else:
                    db.profiles.update_one({"user_id":ctx.author.id}, {'$set':{'is_private':True}})
                    x = "Successfully made your profile private."
            elif data.upper() in noes:
                if old == False:
                    x = "Guess what, your profile is already public. Nothing to change here."
                else:
                    db.profiles.update_one({"user_id":ctx.author.id}, {'$set':{'is_private':False}})
                    x = "Successfully made your profile public."
            else:
                e = discord.Embed(title="Not an option", description="Well that is not a valid option, maybe try again?", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)
            await success(ctx, x)

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rep(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                return await usage(ctx, ['mention a user'], [ctx.author.mention], "Gives the mentioned user a reputation point.")

            if user is ctx.author:
                e = discord.Embed(title="Woah nice try!", description="Sorry but you obviously cannot give yourself reputation points. Better luck next time!", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            if not db.profiles.count({"user_id":user.id}):
                return await error(ctx, "Profile Error", f"{user.name} doesn't have a profile yet. He has to type atleast one message to register a profile.")

            reppers = [x['reppers'] for x in db.profiles.find({"user_id":user.id})][0]
            reppers = [x for x in reppers if x == ctx.author.id]
            if len(reppers) >= 5:
                e = discord.Embed(title=f"Oops that's enough.", description=f"You have already gave {user.name} {len(reppers)} reputation points and that's enough.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            db.profiles.update_one({"user_id":user.id}, {'$inc':{'reputation':1}})
            db.profiles.update_one({"user_id":user.id}, {'$push':{'reppers':ctx.author.id}})


            await success(ctx, f"Successfully gave {user.name} one reputation point.", user.avatar_url)

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def profile_description(self, ctx, *, new: str = None):
        try:
            if new is None:
                return await usage(ctx, ['new description (Max 200 Characters)'], ['Oof master gaddem'], "Lets you edit your profile description.")

            olddesc = [x['description'] for x in db.profiles.find({"user_id":ctx.author.id})][0]
            if len(new) > 200:
                return await error(ctx, "Length Error", "New Description cannot be greater than 200 characters.")
            if olddesc == "None":
                db.profiles.update_one({"user_id":ctx.author.id}, {'$set':{'description':new}})
                return await success(ctx, f"Successfully set your profile description to `{new}`.")
            else:
                e = discord.Embed(title="Just making sure...", description=f"""
This will override your current description.

Current description : `{olddesc}`

Description to change to : `{new}`

If you are sure about this then press :white_check_mark:
If you want to cancel then press :x:
""", color=color())

                footer(ctx, e)
                e.set_thumbnail(url=ctx.me.avatar_url)
                embed_msg = await ctx.send(embed=e)
                await embed_msg.add_reaction('✅')
                await embed_msg.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.author
                try:
                    reaction, message = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
                except asyncio.TimeoutError:
                    return await ctx.send("Since you can't decide which button you should press, I decided to cancel it for you.")

                if str(reaction.emoji) == "✅":
                    db.profiles.update_one({"user_id":ctx.author.id}, {'$set':{'description':new}})
                    return await success(ctx, f"Successfully renewed your profile description to `{new}`.")
                elif str(reaction.emoji) == "❌":
                    can = await ctx.send("Successfully canceled the process cause you pressed :x:")
                    await embed_msg.delete()
                    await asyncio.sleep(8)
                    await can.delete()
                else:
                    can = await ctx.send("Successfully canceled the process cause you added a different reaction.")
                    await embed_msg.delete()
                    await asyncio.sleep(8)
                    await can.delete()

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                user = ctx.author

            if not db.profiles.count({"user_id":user.id}):
                return await error(ctx, "Profile Error", f"{user.name} doesn't have a profile yet. He has to type atleast one message to register a profile.")

            for x in db.profiles.find({"user_id":user.id}):
                is_private = x['is_private']
                if is_private:
                    if user is ctx.author:
                        e = discord.Embed(title="Your profile is private", description="You have decided to set your profile to private. How can you forget about that?", color=color())
                        e.set_thumbnail(url=user.avatar_url)
                        footer(ctx, e)
                        return await ctx.send(embed=e)
                    e = discord.Embed(title="Profile is private", description=f"Sorry but big man {user.name} wants some privacy and has decided to set his profile to be viewed only by him.", color=color())
                    e.set_thumbnail(url=user.avatar_url)
                    footer(ctx, e)
                    return await ctx.send(embed=e)

                e = discord.Embed(title=f"Top Shagger {user.name}", color=color())
                footer(ctx, e)
                e.set_thumbnail(url=user.avatar_url)

                if x['coins'] < 2:
                    coins = f"{x['coins']} Coin"
                else:
                    coins = f"{x['coins']} Coins"

                if x['diamonds'] < 2:
                    diamonds = f"{x['diamonds']} Diamond"
                else:
                    diamonds = f"{x['diamonds']} Diamonds"

                if x['description'] == "None":
                    if user == ctx.author:
                        description = f"Unfortunately you have not yet set a description for your profile. You can set one by using the `{prefix(ctx)}profile_description` command."
                    else:
                        description = f"Unfortunately big lad {user.name} here has not yet set a description for their profile."
                else:
                    description = x['description']

                e.description = f"""
<:gold:514791023671509003> Coins : {coins}
<:starwhite:515866275503931393> XP : {x['xp']}/{x['max_xp']}
<:diagay:515536803407593486> Diamonds : {diamonds}
:speech_left: Messages : {x['messages']}
:arrow_up: Level : {x['level']}
:heart: Reputation : {x['reputation']}
:large_blue_diamond: Achievements : {len(x['achievements'])}

:label: Profile Description : {description}
"""

                await ctx.send(embed=e)

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def avatar(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                return await utils.usage(ctx, ['mention a user'], [ctx.author.mention], 'Returns a user\'s avatar. (Used to fully view a user\'s avatar and download it.)')

            avatar = user.avatar_url
            e = discord.Embed(title="Download Link", url=avatar, color=utils.color())
            e.set_image(url=avatar)
            utils.footer(ctx, e)
            await ctx.send(embed=e)

        except Exception as e:
            await utils.botError(self.bot, ctx, e)

    @commands.command()
    @commands.cooldown(5, 20, commands.BucketType.user)
    async def ping(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                previous = time.time()
                pong = round(self.bot.latency*1000)
                pong_edit = pong
                e = discord.Embed(title=":ping_pong: Pongg!", description=f"It took `{pong}ms` to send this message and `{pong_edit}ms` to edit this message.", color=utils.color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                utils.footer(ctx, e)
                first = await ctx.send(embed=e)
                pong_edit = time.time() - previous
                pong_edit = int(round(pong_edit*1000))
                e = discord.Embed(title=":ping_pong: Pongg!", description=f"It took `{pong}ms` to send this message and `{pong_edit}ms` to edit this message.", color=utils.color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                utils.footer(ctx, e)
                await first.edit(embed=e)
                return
            page = requests.get(user.avatar_url)
            page = page.content
            page = BytesIO(page)
            avatar = Image.open(page).resize((320, 320)).convert('RGBA')
            blank = Image.new('RGBA', (256, 256), color=(231, 19, 29))
            tint = Image.open('assets/red.png').convert('RGBA')
            frames = []
            for i in range(8):
                base = blank.copy()

                if i == 0:
                    base.paste(avatar, (-16, -16), avatar)
                else:
                    base.paste(avatar, (-32 + random.randint(-16, 16), -32 + random.randint(-16, 16)), avatar)

                base.paste(tint, (0, 0), tint)

                frames.append(base) # code stolen from dank memer hehheeeh

                # if i == 0:
                    # base.paste(triggered, (-10, 200))
                # else:
                    # base.paste(triggered, (-12 + randint(-8, 8), 200 + randint(0, 12)))


            b = BytesIO()
            frames[0].save(b, save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2,
                           optimize=True)
            b.seek(0)
            await ctx.send(file=discord.File(b, "ping.gif"))
        except Exception as e:
            await utils.botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))
