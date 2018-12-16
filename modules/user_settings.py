from imports import *

class UserSettings:
    def __init__(self, bot):
        self.bot = bot 
    
    @commands.command()
    async def get_token(self, ctx):
        try:
            if not db.auths.count_documents({"user_id":ctx.author.id}):
                e = discord.Embed(title="Oops you don't have that yet", description=f"Sorry but you have not yet created a token. You can create a token using the `{prefix(ctx)}create_token` command.\n\nWhat are tokens used for?\nTokens are used so that you can access the web dashboard of Overtimed.\nAll you have to do is create your token and go the overtimed website and click log in.\n\nOnce you click log in the bot will then ask you to put your token in.\nAfter that you can now access the web dashboard and you no longer have to put a token the next time you visit the website.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)
            
            token = [x['token'] for x in db.auths.find({"user_id":ctx.author.id})][0]
            e = discord.Embed(title="Here is your token", description=f"`{token}`\nPlease do not share your token with anyone as this can be used to access your web dashboard. To make use of this token, please go to the overtimed website and click log in.", color=color())
            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            await ctx.author.send(embed=e)

        except Exception as e:
            await botError(self.bot, ctx, e)

    @commands.command()
    @commands.cooldown(1, 200, commands.BucketType.user)
    async def create_token(self, ctx):
        try:
            if db.auths.count_documents({"user_id":ctx.author.id}):
                e = discord.Embed(title="Oops you already have that", description=f"Sorry but you have already created a token. You can get that token using the `{prefix(ctx)}get_token` command.", color=color())
                e.set_thumbnail(url=ctx.me.avatar_url)
                footer(ctx, e)
                return await ctx.send(embed=e)
            x = False
            while x is False:
                tokenz = ''.join(random.choices(string.digits + string.ascii_lowercase + string.ascii_uppercase, k=20))
                if not db.auths.count_documents({"token":tokenz}):
                    data = {
                        'user_id':ctx.author.id,
                        'token':tokenz,
                        'username':'',
                        'password':'',
                        'created_at':int(time.time())
                    }
                    guilds = []
                    channels = []
                    for x in self.bot.guilds:
                        for member in x.members:
                            if member == ctx.author:
                                if x not in guilds:
                                    for channel in x.text_channels:
                                        data_up = {
                                            'name':channel.name,
                                            'id':channel.id,
                                            'position':channel.position
                                        }
                                        channels.append(data_up)
                                    guild = x
                                    data = {
                                        'id':guild.id,
                                        'name':guild.name,
                                        'members':guild.members,
                                        'icon_url':guild.icon_url,
                                        'text_channels':channels
                                    }
                                    guilds.append(data)
                                
                    user_data = {
                        'name':ctx.author.name,
                        'discriminator':ctx.author.discriminator,
                        'id':ctx.author.id,
                        'avatar_url':ctx.author.avatar_url,
                        'guilds':guilds
                    }
                    db.auths.insert_one(data)
                    db.user_data.insert_one(user_data)
                    x = True 
            
            e = discord.Embed(title="Successfully created your token", description=f"Here is your token : `{tokenz}`\nPlease do not share your token with anyone as this can be used to access your web dashboard. To make use of this token, please go to the overtimed website and click log in.", color=color())
            e.set_thumbnail(url=ctx.me.avatar_url)
            footer(ctx, e)
            await ctx.author.send(embed=e)

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

def setup(bot):
    bot.add_cog(UserSettings(bot))