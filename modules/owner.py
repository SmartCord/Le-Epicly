from imports import *

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

class OwnerGay:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command()
    async def new_command(self, ctx, category, name, points = None):
        try:
            if points is None:
                points = 0
            else:
                data = {
                    'name':name,
                    'points':points
                }
                db.commands.insert_one(data)
            data = {
                'category':category,
                'command':name,
                'points':points
            }

            db.menu.insert_one(data)
            await ctx.send('done')

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    async def delete_item(self, ctx, command: str, _id: str, *, reason: str):
        try:
            data_shit = {
                'dadjoke':'dadjokes',
                'meme':'memes'
            }
            collection_name = data_shit[command]
            if not db[collection_name].count({"id":_id}):
                return await ctx.send("ID Not found")
            
            for x in db[collection_name].find({"id":_id}):
                data = x
            db[collection_name].delete_one({"id":_id})
            await ctx.send("Deleted yey")

            points = getPoints(command)

            e = discord.Embed(title="Your post was deleted", description=f"Your post : {data['title']} was deleted.\n\nReason : {reason}\nPoints given back : {points}", color=color())
            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            user = discord.utils.get(self.bot.get_all_members(), id=data['uploaded_by'])
            if user is None:
                return 
            
            await user.send(embed=e)
            db.profiles.update_one({"user_id":user.id}, {'$inc':{'points':points}})
            

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    @commands.is_owner()
    async def start_programmer_humor_uploads(self, ctx, rangexddd: int):
        try:
            total = len([x for x in db.programmer_humor.find({})])
            messagex = await ctx.send(f"""
Updating the database, Total programmer_humor = {total};

None
""")

            for post in reddit.subreddit('ProgrammerHumor').new(limit=rangexddd):
                title = post.title
                image = post.url
                source = "https://www.reddit.com" + post.permalink
                if not post.stickied and post.selftext == "" or post.selftext == " ":

                    data = {
                        'id':str(uuid.uuid4()),
                        'title':title,
                        'description':'None',
                        'source':source,
                        'image':image,
                        'uploaded_by':self.bot.user.id
                    }

                    if not db.programmer_humor.count({"source":source}):
                        db.programmer_humor.insert_one(data)
                        message = f"Uploaded contents of : `{source}`"
                    else:
                        message = "Source already in DB : " + '`' + source + '`'
                    print(message)
                    total = len([x for x in db.programmer_humor.find({})])
                    await messagex.edit(content=f"""
    Updating the database, Total programmer_humor = {total};

    {message}
    """)
                    await asyncio.sleep(1)

            await messagex.edit(content="Cleaning up...")
            deleted_for_title = []
            deleted_for_description = []
            for x in db.programmer_humor.find({}):
                if len(x['title']) > 254:
                    db.programmer_humor.delete_one({"id":x['id']})
                    deleted_for_title.append(x['id'])

                if x['description'] == "" or x['description'] == " ":
                    db.programmer_humor.delete_one({"id":x['id']})
                    deleted_for_description.append(x['id'])

            await messagex.edit(content=f"Finished cleaning up.\nDeleted for long title : {len(deleted_for_title)}\nDeleted for no description : {len(deleted_for_description)}")

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    @commands.is_owner()
    async def start_dadjoke_uploads(self, ctx, rangelol: int):
        try:
            total = len([x for x in db.dadjokes.find({})])
            messagex = await ctx.send(f"""
Updating the database, Total dadjokes = {total};

None
""")

            for post in reddit.subreddit('dadjokes').new(limit=rangelol):
                title = post.title
                description = post.selftext
                source = post.url
                data = {
                    'id':str(uuid.uuid4()),
                    'title':title,
                    'description':description,
                    'source':source,
                    'image':'None',
                    'uploaded_by':self.bot.user.id
                }

                if not db.dadjokes.count({"source":source}):
                    db.dadjokes.insert_one(data)
                    message = f"Uploaded contents of : `{source}`"
                else:
                    message = "Source already in DB : " + '`' + source + '`'
                print(message)
                total = len([x for x in db.dadjokes.find({})])
                await messagex.edit(content=f"""
Updating the database, Total dadjokes = {total};

{message}
""")
                await asyncio.sleep(1)

            await messagex.edit(content="Cleaning up...")
            deleted_for_title = []
            deleted_for_description = []
            for x in db.dadjokes.find({}):
                if len(x['title']) > 254:
                    db.dadjokes.delete_one({"id":x['id']})
                    deleted_for_title.append(x['id'])

                if x['description'] == "" or x['description'] == " ":
                    db.dadjokes.delete_one({"id":x['id']})
                    deleted_for_description.append(x['id'])

            await messagex.edit(content=f"Finished cleaning up.\nDeleted for long title : {len(deleted_for_title)}\nDeleted for no description : {len(deleted_for_description)}")

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    @commands.is_owner()
    async def start_meme_uploads(self, ctx, rangexxx: int):
        try:
            url = "https://api.ksoft.si/images/random-meme"
            token = config.ksoft
            total = len([x for x in db.memes.find({})])
            messagex = await ctx.send(f"""
Updating the database, Total memes = {total};

None
""")

            for eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee in range(rangexxx):
                async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {token}"}) as cs:
                    async with cs.get(url) as rep:
                        x = await rep.json()

                data = {
                    'id':str(uuid.uuid4()),
                    'title':x['title'],
                    'source':x['source'],
                    'image':x['image_url'],
                    'uploaded_by':'KSoft API'
                }

                if not db.memes.count({"source":x['source']}):
                    db.memes.insert_one(data)
                    message = f"Uploaded contents of : `{x['source']}`"
                else:
                    message = "Source already in DB : " + '`' + x['source'] + '`'
                print(message)
                total = len([x for x in db.memes.find({})])
                await messagex.edit(content=f"""
Updating the database, Total memes = {total};

{message}
""")
                await asyncio.sleep(1)

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command(pass_context=True, name="eval")
    @commands.is_owner()
    async def cool_eval_bullshit(self, ctx, *, body: str):
        try:
            """ Code from R.Danny bot yeyey k, modified to fit my other bullshit """
            env = {
                'self':self,
                'ctx':ctx,
                'db':db,
                'discord':discord
            }
            env.update(globals())
            body = cleanup_code(body)
            std = io.StringIO()
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
            try:
                exec(to_compile, env)
            except Exception as e:
                return await ctx.send(f'```py\n{e}\n```')

            func = env['func']

            try:
                with redirect_stdout(std):
                    ret = await func()
            except Exception as e:
                value = std.getvalue()
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = std.getvalue()
                try:
                    await ctx.message.add_reaction('\u2705')
                except:
                    pass
                if ret is None:
                    if value:
                        await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')

        except Exception as e:
            await utils.botError(self.bot, ctx, e)


    @commands.command()
    @commands.is_owner()
    async def client_edit(self, ctx, *, new_name: str = None):
        try:
            if new_name is None:
                return await utils.usage(ctx, ['new name'], ['you gay men'], 'Lets you change the bot\'s actual name (Not nickname).')

            await self.bot.user.edit(username=new_name)
            await utils.success(ctx, "Successfully changed the name to {}".format(new_name))

        except Exception as e:
            await utils.botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(OwnerGay(bot))
