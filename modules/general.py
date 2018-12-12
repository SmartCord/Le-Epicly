from imports import *

class GeneralCommands:
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
        self.purchases = []

    @commands.command()
    async def gay(self, ctx, *, user: discord.Member = None):
        try:
            if user is None:
                user = ctx.author
                 
            random.seed(user.id)
            percentage = random.randint(1, 100)
            e = discord.Embed(title=f"Here is the gay rate of {user.name}", description=f"{percentage}% Gay", color=color())
            e.set_thumbnail(url=user.avatar_url)
            footer(ctx, e)
            await ctx.send(embed=e)
        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def help(self, ctx):
        try:
            e = discord.Embed(title="Welcome to the one and only amazing spectacular unbelievably interactive help command.", color=color())
            e.description = """
In this documentation you will learn how to use the discord bot correctly.

Some commands (Specifically fun commands) requires points. If you don't have enough points
the bot will tell you that (Obviously). To purchase points you have to look at the store (Stare at it's soul) and then once
you find the item/points pack you want to purchase simply use the purchase command.

Each command has a category and to access a category press one of the reactions below this embed.

❓ - This menu
💠 - General Commands 
🔧 - Utility Commands
😂 - Fun Commands
⚙ - User Settings 

"""

            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            menu = await ctx.send(embed=e)
            reactions = ['❓', '💠', '🔧', '😂', '⚙']
            for reaction in reactions:
                await menu.add_reaction(reaction)
            
            def check(reaction, user):
                return user == ctx.author

            async def commandGet(category):
                if category == "user_settings":
                    namex = "User Settings"
                else:
                    namex = category[0].upper() + category[1:]
                embed = discord.Embed(title=f"{namex} Commands", color=color())
                embed.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, embed)
                server_prefix = prefix(ctx)
                embed.description = ""
                for x in db.menu.find({"category":category}):
                    embed.description += f"{server_prefix}{x['command']}\n:small_orange_diamond: Points : {x['points']}\n\n"

                return embed

            doFunction = {
                '❓':'menu',
                '💠':'general',
                '🔧':'utility',
                '😂':'fun',
                '⚙':'user_settings'
            }
            
            while True:
                reaction, message = await self.bot.wait_for('reaction_add', check=check)
                if str(reaction.emoji) == "❓":
                    await menu.edit(embed=e)
                else:
                    try:
                        embed = await commandGet(doFunction[str(reaction.emoji)])
                        await menu.edit(embed=embed)
                        try:
                            await menu.remove_reaction(str(reaction.emoji), ctx.author)
                        except:
                            pass
                    except KeyError:
                        pass

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command(aliases=['programmer_humour'])
    async def programmer_humor(self, ctx):
        try:
            if await pointless(ctx):
                return

            humors = [x for x in db.programmer_humor.find({})]
            humor = random.choice(humors)
            image = humor['image']
            title = humor['title']
            source = humor['source']
            uploaded_by = humor['uploaded_by']
            id = humor['id']

            uploaded_by = discord.utils.get(self.bot.get_all_members(), id=uploaded_by)
            if uploaded_by is None:
                uploaded_by = "User cannot be found"
                avatar = self.bot.user.avatar_url
            else:
                avatar = uploaded_by.avatar_url

            e = discord.Embed(title=title, url=source, color=color())
            e.set_image(url=image)
            e.set_footer(text="Uploaded by : {}".format(uploaded_by), icon_url=avatar)
            await ctx.send(embed=e)

            if not db.programmer_humor_collection.count({"id":id, "user_id":ctx.author.id}):
                db.programmer_humor_collection.insert_one({"id":id, "user_id":ctx.author.id})

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command(aliases=['programmer_humour_collection'])
    async def programmer_humor_collection(self, ctx):
        try:
            if not db.programmer_humor_collection.count({"user_id":ctx.author.id}):
                e = discord.Embed(title="You don't have any of those things yet", description=f"Please use the `{prefix(ctx)}programmer_humor` command atleast once.", color=color())
                footer(ctx, e)
                e.set_thumbnail(url=ctx.me.avatar_url)
                return await ctx.send(embed=e)

            embeds = []
            for x in db.programmer_humor_collection.find({"user_id":ctx.author.id}):
                for y in db.programmer_humor.find({"id":x['id']}):
                    e = discord.Embed(title=y['title'], url=y['source'], color=color())
                    e.set_image(url=y['image'])
                    footer(ctx, e)
                    embeds.append(e)

            p = paginator.EmbedPages(ctx, embeds=embeds)
            await p.paginate()

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def my_dadjokes(self, ctx):
        try:
            if not db.dadjokes.count({"uploaded_by":ctx.author.id}):
                e = discord.Embed(title="Oh you don't have any yet :(", description=f"Sorry but you have not yet uploaded a dad joke. You can upload your first dad joke using the `{prefix(ctx)}upload_dadjoke` command.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            jokes = [x for x in db.dadjokes.find({"uploaded_by":ctx.author.id})]
            embeds = []

            for joke in jokes:
                title = joke['title']
                description = joke['description']
                source = joke['source']
                if source is 'None':
                    source = None

                e = discord.Embed(title=title, description=description, color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                embeds.append(e)

            p = paginator.EmbedPages(ctx, embeds=embeds)
            await p.paginate()

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def upload_dadjoke(self, ctx, *, arguments: str = None):
        try:
            if await pointless(ctx):
                return

            if arguments is None:
                return await usage(ctx, ['arguments'], ['title=Why was the broom late to work;; description=It overswept'], 'Available arguments are title and description. To seperate arguments use ";;" (See example above)')

            arguments = arguments.split(";;")
            args = {}
            for item in arguments:
                item_u = item.upper()
                title_start = ("TITLE=", " TITLE=")
                description_start = ("DESCRIPTION=", " DESCRIPTION=")

                if item_u.startswith(title_start):
                    title_cut = item[6:]
                    if title_cut.startswith("="):
                        title_cut = item[7:]
                    args['title'] = title_cut

                if item_u.startswith(description_start):
                    description_cut = item[12:]
                    if description_cut.startswith("="):
                        description_cut = item[13:]
                    args['description'] = description_cut

            args_list = args.keys()
            if not 'title' in args_list and not 'description' in args_list:
                e = discord.Embed(title="Oops I can't find any valid arguments", description="The valid arguments are title and description.\n Here is an example of how the command works `title=Why was the broom late to work;; description=It overswept`. \nTo seperate arguments use ';;' (Obviously without the quotation marks)", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            if not 'title' in args_list and 'description' in args_list:
                e = discord.Embed(title="Uhh you missed one argument?", description="You missed the title argument...", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            if 'title' in args_list and not 'description' in args_list:
                e = discord.Embed(title="Uhh you missed one argument?", description="You missed the description argument...", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            title = args['title']
            description = args['description']
            uploaded_by = ctx.author.id
            id = str(uuid.uuid4())

            data = {
                'id':id,
                'title':title,
                'description':description,
                'source':'None',
                'image':'None',
                'uploaded_by':uploaded_by
            }
            db.dadjokes.insert_one(data)
            await success(ctx, f"Successfully uploaded your dadjoke\nTitle : {title}\nDescription : {description}")

            channel_to_send = self.bot.get_channel(522268395807440917)
            author_sender = discord.utils.get(self.bot.get_all_members(), id=data['uploaded_by'])
            e = discord.Embed(title=data['title'], description=data['description'], color=color())
            e.set_thumbnail(url=author_sender.avatar_url)
            e.set_footer(text=data['id'])
            await channel_to_send.send(embed=e)

            niggas = db.dadjokes.count({"uploaded_by":ctx.author.id})
            if niggas == 10:
                await giveAchievement(ctx.author, 5, extra="for uploading 10 dad jokes")


        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def dadjoke_collection(self, ctx):
        try:
            if not db.dadjoke_collection.count({"user_id":ctx.author.id}):
                e = discord.Embed(title="Oops it's empty", description=f"Sorry but you haven't seen any dad jokes from this bot yet. Use the `{prefix(ctx)}dadjoke` command atleast once.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            embeds = []
            for x in db.dadjoke_collection.find({"user_id":ctx.author.id}):
                for y in db.dadjokes.find({"id":x['id']}):
                    e = discord.Embed(title=y['title'], description=y['description'], color=color())
                    if y['source'] != 'None':
                        e.url = y['source']
                    e.set_thumbnail(url=ctx.me.avatar_url)
                    footer(ctx, e)
                    embeds.append(e)

            p = paginator.EmbedPages(ctx, embeds=embeds)
            await p.paginate()

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dadjoke(self, ctx, ranged: str = None):
        try:
            if await pointless(ctx):
                return

            if ranged is None:
                ranged = 1

            try:
                ranged = int(ranged)
            except:
                e = discord.Embed(title="The range should be an integer", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            if ranged > 10 or ranged < 1:
                e = discord.Embed(title="Woah hold on right there", description="The maximum range for this command is 10 and the minimum is 1.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            jokes = []
            shits = [x for x in db.dadjokes.find({})]

            for x in range(ranged):
                joke = random.choice(shits)
                if not joke in jokes:
                    jokes.append(joke)

            embeds = []

            for joke in jokes:
                user = discord.utils.get(self.bot.get_all_members(), id=joke['uploaded_by'])
                if user is None:
                    user = "User cannot be found"
                    avatar = ctx.me.avatar_url
                else:
                    avatar = user.avatar_url

                title = joke['title']
                description = joke['description']
                e = discord.Embed(title=title, description=description, color=color())
                source = joke['source']

                if source != 'None':
                    e.url = source


                e.set_thumbnail(url=ctx.me.avatar_url)
                e.set_footer(text=f"Uploaded by : {user}", icon_url=avatar)
                embeds.append(e)
                if not db.dadjoke_collection.count({"user_id":ctx.author.id, "id":joke['id']}):
                    db.dadjoke_collection.insert_one({"user_id":ctx.author.id, "id":joke['id']})

            seen = db.dadjoke_collection.count({"user_id":ctx.author.id})
            if seen == 300:
                await giveAchievement(ctx.author, 6, extra="for using the dad joke command 300 times")

            p = paginator.EmbedPages(ctx, embeds=embeds)
            await p.paginate()

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command() # 30 points
    @commands.cooldown(2, 15, commands.BucketType.user)
    async def upload_meme(self, ctx, url: str = None):
        try:
            if await pointless(ctx):
                return

            if url is None:
                return await usage(ctx, ['reddit url'], ['https://www.reddit.com/r/dankmemes/comments/a372j6/bring_home_the_bagels/'], 'Lets you upload a meme to the overtimed meme database. (Only reddit links are currently supported for now)')

            if not url.startswith('https://www.reddit.com/r/'):
                if url.startswith('https://www.reddit.com/u/'):
                    return await error(ctx, "Invalid URL", "Please provide a reddit post url not a user one.")
                return await error(ctx, "Invalid URL", "Please provide a reddit post url.")

            if not url.endswith('/'):
                url += "/"


            # proxies = utils.get_proxies()
            #chosen = random.choice(proxies)
            # connection = False
            # for chosen in proxies:
                # user_agent = random.choice(utils.user_agents)
                # proxy = {
                    # "http": f'http://{chosen}',
                    # "https": f'http://{chosen}'
                # }
                # try:
                    # r = requests.get(url, headers=user_agent, proxies=proxy)
                    # break #lol
                # except:
                    # pass


            user_agent = random.choice(utils.user_agents)
            r = requests.get(url, headers=user_agent)

            page = r.text
            soup = bsoup(page, 'html.parser')
            source = url
            uploaded_by = ctx.author.id
            id = str(uuid.uuid4())
            channel_to_send = self.bot.get_channel(522261757817913354)
            try:
                title = soup.find('span', attrs={'class':'y8HYJ-y_lTUHkQIc1mdCq'}).text
                image = soup.find('div', attrs={'class':'_3Oa0THmZ3f5iZXAQ0hBJ0k'})
                image = image.find('a')
                image = image['href']
            except:
                try:
                    source_id = source.split('comments/')[1].split('/')[0]
                    submission = reddit.submission(id=source_id)
                    title = submission.title
                    image = submission.url
                except:
                    return await error(ctx, "Invalid URL", "The reddit post you provided is invalid.") #

            if db.memes.count({"source":source}):
                meme = [x['uploaded_by'] for x in db.memes.find({"source":source})][0]
                e = discord.Embed(color=color())
                if meme == "KSoft API":
                    e.title = "Oops an API have already uploaded that :("
                    e.description = "Sad to say but KSoft API have already uploaded that meme."
                elif meme == ctx.author.id:
                    e.title = "You already uploaded that..."
                    e.description = f"Sorry but you have already uploaded that meme."
                elif isinstance(meme, int):
                    user = discord.utils.get(self.bot.get_all_members(), id=meme)
                    if user is None:
                        e.title = "That meme has already been uploaded by an unknown user"
                        e.description = f"Unfortunately an unknown user with the id `{meme}` have already uploaded that meme."
                    else:
                        e.title = f"That meme has already been uploaded by {user}"
                        e.description = f"Sorry but {user} have already uploaded that meme. Better luck next time :)"
                footer(ctx, e)
                e.set_thumbnail(url=ctx.author.avatar_url)
                return await ctx.send(embed=e)

            data = {
                'id':id,
                'title':title,
                'source':source,
                'image':image,
                'uploaded_by':uploaded_by
            }
            db.memes.insert_one(data)

            await success(ctx, f"Successfully uploaded that [cool meme]({source}) to the meme database.", image)
            uploaded = len([x for x in db.memes.find({"uploaded_by":ctx.author.id})])
            author = discord.utils.get(self.bot.get_all_members(), id=data['uploaded_by'])
            e = discord.Embed(title=data['title'], url=data['source'], color=color())
            e.set_thumbnail(url=author.avatar_url)
            e.set_image(url=data['image'])
            e.set_footer(text=data['id'])
            await channel_to_send.send(embed=e)
            if uploaded == 10:
                await giveAchievement(ctx.author, 2, extra="for uploading 10 memes")

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def meme_collection(self, ctx):
        try:
            if not db.meme_collection.count({"user_id":ctx.author.id}):
                e = discord.Embed(title="Collection empty", description=f"Your meme collection is empty, you have to use the `{prefix(ctx)}meme` command atleast once.", color=color())
                e.set_thumbnail(url=ctx.author.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            embeds = []
            for y in db.meme_collection.find({"user_id":ctx.author.id}):
                for x in db.memes.find({"id":y['id']}):
                    e = discord.Embed(title=x['title'], url=x['source'], color=color())
                    e.set_image(url=x['image'])
                    footer(ctx, e)
                    embeds.append(e)

            p = paginator.EmbedPages(ctx, embeds=embeds)
            await p.paginate()

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def my_memes(self, ctx):
        try:
            if not db.memes.count({"uploaded_by":ctx.author.id}):
                e = discord.Embed(title="Sad no memes", description=f"Sorry but you have not yet uploaded any memes. You can upload one by using the `{prefix(ctx)}upload_meme` command.", color=color())
                e.set_thumbnail(url=ctx.author.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            embeds = []
            for x in db.memes.find({"uploaded_by":ctx.author.id}):
                e = discord.Embed(title=x['title'], url=x['source'], color=color())
                e.set_image(url=x['image'])
                footer(ctx, e)
                embeds.append(e)

            p = paginator.EmbedPages(ctx, embeds=embeds)
            await p.paginate()

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command() # 4 points
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def meme(self, ctx):
        try:
            if await pointless(ctx):
                return

            memes = [y for y in db.memes.find({})]
            x = random.choice(memes)

            e = discord.Embed(title=f"{x['title']}", url=x['source'], color=color())
            e.set_image(url=x['image'])
            if x['uploaded_by'] ==  "KSoft API":
                by = "From KSoft API"
                icon_url = "https://cdn.ksoft.si/images/Logo1024-W.png"
            elif isinstance(x['uploaded_by'], int):
                xd = discord.utils.get(self.bot.get_all_members(), id=x['uploaded_by'])
                if xd is None:
                    by = "User cannot be found"
                    icon_url = ctx.me.avatar_url
                else:
                    by = f"Uploaded by : {xd}"
                    icon_url = xd.avatar_url

            e.set_footer(text=by, icon_url=icon_url)
            await ctx.send(embed=e)

            data = {
                'id':x['id'],
                'user_id':ctx.author.id
            }

            if db.meme_collection.count(data):
                pass
            else:
                db.meme_collection.insert_one(data)

            seens = len([x for x in db.meme_collection.find({"user_id":ctx.author.id})])
            if seens == 500:
                await giveAchievement(ctx.author, 3, extra="for using the meme command 500 times")

        except Exception as e:
            await botError(self.bot, ctx, e)

    # @commands.command()
    # @commands.cooldown
    # async def points(self, ctx, user: discord.Member = None):
        # try:
            # if user is None:
                # user = ctx.author
#
            # if not db.profiles.find({"user_id":user.id}):
                # return await error(ctx, "Profile Error", f"{user.name} doesn't have a profile yet. He has to type atleast one message to register a profile.")
#
            # for x in db.profiles.find({"user_id":user.id}):
                # is_private = x['is_private']
                # if is_private:
                    # if user is ctx.author:
                        # e = discord.Embed(title="Your profile is private", description="You have decided to set your profile to private. How can you forget about that?", color=color())
                        # e.set_thumbnail(url=user.avatar_url)
                        # footer(ctx, e)
                        # return await ctx.send(embed=e)
                    # e = discord.Embed(title="Profile is private", description=f"Sorry but big man {user.name} wants some privacy and has decided to set his profile to be viewed only by him.", color=color())
                    # e.set_thumbnail(url=user.avatar_url)
                    # footer(ctx, e)
                    # return await ctx.send(embed=e)
#
                # memes = x['memes']
                # upload_memes = x['upload_memes']
#
            # title = "Here all of your points."
            # if user != ctx.author:
                # title = f"Here are all of {user.name}'s points."
#
            # e = discord.Embed(title=title, color=color()).set_thumbnail(url=user.avatar_url)
            # e.description = f"""
# :small_orange_diamond: Memes : {memes}
# :small_orange_diamond: Upload Memes : {upload_memes}
# """
            # footer(ctx, e)
            # await ctx.send(embed=e)
#
        # except Exception as e:
            # await botError(self.bot, ctx, e)

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

    @commands.command()
    @commands.cooldown(2, 100, commands.BucketType.user)
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
    @commands.cooldown(2, 300, commands.BucketType.user)
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
                e = discord.Embed(title="Just making sure you know", description=f"""
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
