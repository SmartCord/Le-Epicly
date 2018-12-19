from imports import *

class FunCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, *, question: str = None):
        try:
            if await pointless(ctx):
                return 

            if question is None:
                return await usage(ctx, ['question'], ['Why is puberty a thing?'], 'Returns an "honest" answer for your question.')
            
            if question.upper().startswith(("WHY", " WHY")):
                choices = [
                    'Because why not?',
                    "Because thor didn't go for the head.",
                    "Because that's just the reality.",
                    "Because that's what I want.",
                    "Because that's just the truth.",
                    "Because that's the thing everyone wanted.",
                    "Because that's just really the case."
                ]
            else:
                choices = [
                    "YES!",
                    "NO!",
                    "Lmaooo no",
                    "Hell yes",
                    "NAhhhh"
                ]

            await Embed(ctx, question, random.choice(choices))

        except Exception as e:
            await botError(self.bot, ctx, e)
    
    @commands.command(name="8ball")
    async def ball8(self, ctx, *, question: str = None):
        try:

            if await pointless(ctx):
                return

            if question is None:
                return await usage(ctx, ['question'], ['am i gay?'], 'Lets you ask the 8ball.')
            
            answers = [
                'It is certain',
                'It is decidedly so',
                'Without a doubt',
                'Yes',
                'You may rely on it',
                'As I see it, yes',
                'Most likely',
                "Don't count on it",
                'My reply is no',
                'My sources say no',
                'Outlook not so good',
                'Very doubtful'
            ]
            mentions = ctx.message.mentions 
            shits = []
            if mentions != []:
                for mention in mentions:
                    for item in question.split():
                        ix = item.replace(mention.mention, mention.name)
                        shits.append(ix)
            else:
                shits = question.split()

            question = " ".join(shits)
            question = question.upper().replace("AM I", f"Is {ctx.author.name}").lower()
            question = question[0].upper() + question[1:]
            question_lil = question.replace("?", "").replace(".", "").replace('"', "").replace("'", "").replace(",", "").replace(" ", "").upper()
            random.seed(question_lil)
            e = discord.Embed(title=question, description=f":8ball: {random.choice(answers)}", color=color())
            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            await ctx.send(embed=e)

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def penis(self, ctx, *, user: discord.Member = None):
        try:
            if await pointless(ctx):
                return 

            if user is None:
                user = ctx.author
            
            random.seed(user.id)
            size = "=" * random.randint(1, 30)
            e = discord.Embed(title=f"Here is {user.name}'s ding dong size", description=f"8{size}D", color=color())
            e.set_thumbnail(url=user.avatar_url)
            footer(ctx, e)
            await ctx.send(embed=e)
            if not db.command_log_counter.count_documents({"user_id":ctx.author.id, "command":"penis"}):
                data = {
                    'user_id':ctx.author.id,
                    'command':'penis'
                }
                db.command_log_counter.insert_one(data)
                await giveAchievement(ctx.author, 8, extra="for using the penis command once")
        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command(aliases=['gay_rate', 'gayrate'])
    async def gay(self, ctx, *, user: discord.Member = None):
        try:

            if await pointless(ctx):
                return 

            if user is None:
                user = ctx.author

            random.seed(user.id)
            percentage = random.randint(1, 100)
            title = f"Here is {user.name}'s gay rate"
            if user is ctx.author:
                title = "Here is your gay rate"
            e = discord.Embed(title=title, description=f"{percentage}% Gay", color=color())
            e.set_thumbnail(url=user.avatar_url)
            footer(ctx, e)
            await ctx.send(embed=e)
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
    async def upload_meme(self, ctx, *, title: str = None):
        try:
            if await pointless(ctx):
                return

            if title is None:
                return await usage(ctx, ['title', 'attach an image file (Attachment, not a link)'], ['this guy drunk lmao', '*attaches an image of a drunk kid*'], 'Lets you upload a meme. Duh')

            if ctx.message.attachments == []:
                return await usage(ctx, ['title', 'attach an image file (Attachment, not a link)'], ['this guy drunk lmao', '*attaches an image of a drunk kid*'], 'Lets you upload a meme. Duh')


            url = ctx.message.attachments[0].url
            images_suffix = ('png', 'jpg', 'jpeg')
            if not url.endswith(images_suffix):
                e = discord.Embed(title="Attachment not an image", description="Your attachment should be an image.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)

            id = str(uuid.uuid4())

            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as rp:
                    content = rp.content 
            
            image = BytesIO(content)
            image = Image.open(image).convert('RGBA')
            f = BytesIO()
            image.save(f, 'png')
            f.seek(0)
            channel = self.bot.get_channel(522261757817913354)
            await channel.send(file=discord.File(f, 'cool.png'), content=f"ID : {id}")


            data = {
                'id':id,
                'title':title,
                'image':image,
                'uploaded_by':ctx.author.id
            }
            db.memes.insert_one(data)
            await success(ctx, f"Successfully uploaded that cool meme to the meme database.", image)
            uploaded = len([x for x in db.memes.find({"uploaded_by":ctx.author.id})])
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
    
def setup(bot):
    bot.add_cog(FunCommands(bot))