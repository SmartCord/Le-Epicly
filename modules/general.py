from imports import *

class GeneralCommands:
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

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
                e.set_thumbnail(url=utils.gif['hmm1'])
                embed_msg = await ctx.send(embed=e)
                await embed_msg.add_reaction('✅')
                await embed_msg.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.author
                try:
                    reaction = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
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
                    return await error(ctx, "Profile Error", f"Sorry but big man {user.name} wants some privacy and has decided to set his profile to be viewed only by him.")

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

:exclamation: Profile Description : {description}
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
