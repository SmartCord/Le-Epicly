from imports import *

class GeneralCommands:
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
        self.purchases = []

    @commands.command()
    async def help(self, ctx, *, category: str = None):
        try:
            e = discord.Embed(title="Welcome to the one and only amazing spectacular unbelievably interactive help command.", color=color())
            e.description = f"""
In this documentation you will learn how to use the discord bot correctly.

Some commands (Specifically fun commands) requires points. If you don't have enough points
the bot will tell you that (Obviously). To purchase points you have to look at the store (Stare at it's soul) and then once
you find the item/points pack you want to purchase simply use the purchase command.

Each command has a category and to access a category press one of the reactions below this embed.
Alternatively you can type `{prefix(ctx)}help category_name_here`

💠 - General Commands 
🔧 - Utility Commands
😂 - Fun Commands
⚙ - User Settings 

"""

            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            menu = await ctx.send(embed=e)
            reactions = ['💠', '🔧', '😂', '⚙']
            for reaction in reactions:
                await menu.add_reaction(reaction)
            
            def check(reaction, user):
                return user == ctx.author

            async def commandGet(category):
                if category == "user_settings":
                    namex = "User Settings"
                else:
                    namex = category[0].upper() + category[1:]
                
                pg = commands.Paginator(prefix="", suffix="", max_size=500)
                server_prefix = prefix(ctx)

                for x in db.menu.find({"category":category}):
                    s = "s"
                    if x['points'] < 2:
                        s = ""

                    #embed.description += f"`{server_prefix}{x['command']} ({x['points']} Point{s})`, "
                    #embed.description += f"{server_prefix}{x['command']} - {x['points']} Point{s}\n"
                    pg.add_line(f"{server_prefix}{x['command']}\n:small_orange_diamond: Point{s} : {x['points']}\n")

                embeds = []
                for page in pg.pages:
                    embed = discord.Embed(title=f"{namex} Commands", description=page, color=color())
                    embed.set_thumbnail(url=ctx.me.avatar_url)
                    footer(ctx, embed)
                    embeds.append(embed)

                p = paginator.EmbedPages(ctx, embeds=embeds)
                return p

            doFunction = {
                '❓':'menu',
                '💠':'general',
                '🔧':'utility',
                '😂':'fun',
                '⚙':'user_settings'
            }
            if category != None:
                ifwork = False
                user_input = category.replace("_", " ")
                data = {
                    'General Commands':'general',
                    'Utility Commands':'utility',
                    'Fun Commands':'fun',
                    'User Settings':'user_settings'
                }
                for x in data.keys():
                    similarity = utils.CheckStringSimilarity(x.upper(), user_input.upper())
                    if similarity >= 0.7:
                        p = await commandGet(data[x])
                        await menu.delete()
                        await p.paginate()
                        ifwork = True
                if not ifwork:
                    await ctx.send("Sorry but that's an invalid category, please check the list above")

            yyy = True
            while yyy is True:
                reaction, message = await self.bot.wait_for('reaction_add', check=check)
                try:
                    p = await commandGet(doFunction[str(reaction.emoji)])
                    await menu.delete()
                    await p.paginate()
                    yyy = False
                except KeyError:
                    pass

                # try:
                #     await menu.remove_reaction(str(reaction.emoji), ctx.author)
                # except:
                #     pass
                # if str(reaction.emoji) == "❓":
                #     await menu.edit(embed=e)
                # else:
                #     try:
                #         await commandGet(doFunction[str(reaction.emoji)])
                #         False
                #     except KeyError:
                #         pass

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command(aliases=['shop'])
    @commands.cooldown(1, 10, commands.BucketType.user)
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
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def buy(self, ctx, *, item: str = None):
        try:
            if item is None:
                return await usage(ctx, ['item name'], ['i like memes'], 'Lets you purchase an item from the store.')

            item = item.upper()
            appended_data = [ctx.author.id, ctx.channel.id]

            if not db.store.count({"name_upper":item}):
                e = discord.Embed(title="That item doesn't exist", description="Sorry mate but the item you entered doesn't exist. Please make sure the spelling is correct and there are no extra characters.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            ongoing = False
            for i in self.purchases:
                if ctx.author.id in i:
                    ongoing = True
                    channel_id = i[1]
                    break

            if ongoing:
                channel = discord.utils.get(self.bot.get_all_channels(), id=channel_id)
                if not channel is None:
                    guild = channel.guild
                    e = discord.Embed(title="You currently have an ongoing purchase", color=color())
                    footer(ctx, e)
                    e.set_thumbnail(url=ctx.author.avatar_url)
                    if channel == ctx.channel:
                        e.description = f"You currently have an ongoing purchase in this specific channel. Please finish that purchase or wait for it to time out."
                    elif guild == ctx.guild:
                        e.description = f"You currently have an ongoing purchase in the channel {channel.mention}. Please finish that purchase or wait for it to time out."
                    else:
                        e.description = f"You currently have an ongoing purchase in the channel {channel.name} in the server {guild.name}. Please finish that purchase or wait for it to time out."

                    return await ctx.send(embed=e)
                self.purchases.remove(appended_data)



            perks = []

            for x in db.store.find({"name_upper":item}):
                name = x['name']
                coins = x['coins']
                diamonds = x['diamonds']
                try:
                    perks.append(['points', x['points']])
                    break
                except:
                    pass

                # try:
                    # perks.append(['upload_memes', x['upload_memes']])
                    # break
                # except:
                    # pass

            coin = self.bot.get_emoji(514791023671509003)
            diamond = self.bot.get_emoji(515536803407593486)
            e = discord.Embed(title="What do you want to purchase with?", description=f"Choose by clicking one of the reactions below.\n{coin} Price on coins : {coins}\n{diamond} Price on diamonds : {diamonds}", color=color())
            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            embed = await ctx.send(embed=e)
            await embed.add_reaction(coin)
            await embed.add_reaction(diamond)

            self.purchases.append(appended_data)

            def check(reaction, user):
                return user == ctx.author

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
                if 'points' in i:
                    data = {'$inc':{'points':i[1]}}
                # elif 'upload_memes' in i:
                    # data = {'$inc':{'upload_memes':i[1]}}

            tries = []

            while x is False:
                if x is False:
                    try:
                        reaction, message = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
                    except asyncio.TimeoutError:
                        self.purchases.remove(appended_data)
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
                                self.purchases.remove(appended_data)
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
                                self.purchases.remove(appended_data)
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
                    self.purchases.remove(appended_data)
                    await embed_msg.delete()
                    await asyncio.sleep(8)
                    await can.delete()
                    return

            await success(ctx, f"Successfully purchased the item `{name}`, {message}")
            self.purchases.remove(appended_data)

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command() # 4 points
    @commands.cooldown(2, 50, commands.BucketType.user)
    async def rep(self, ctx, *, user: discord.Member = None):
        try:
            if await pointless(ctx):
                return

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
    @commands.cooldown(1, 4, commands.BucketType.user)
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

                memes_uploaded = 0
                if db.memes.count({"uploaded_by":user.id}):
                    memes_uploaded = len([x for x in db.memes.find({'uploaded_by':user.id})])

                e.description = f"""
<:gold:514791023671509003> Coins : {coins}
<:starwhite:515866275503931393> XP : {x['xp']}/{x['max_xp']}
<:diagay:515536803407593486> Diamonds : {diamonds}
:speech_left: Messages : {x['messages']}
:arrow_up: Level : {x['level']}
:heart: Reputation : {x['reputation']}
:large_blue_diamond: Achievements : {len(x['achievements'])}
:small_orange_diamond: Points : {x['points']}
<:mad:520157535680987167> Memes Uploaded : {memes_uploaded}

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
            await giveAchievement(ctx.author, 1, extra="for finding a hidden feature on the command ping")
            await ctx.send(file=discord.File(b, "ping.gif"))
        except Exception as e:
            await utils.botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))
