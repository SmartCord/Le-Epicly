from imports import *

class Tracker:
    def __init__(self, bot):
        self.bot = bot
        self.antispam = []

    async def antiSpam(self, user):
        await asyncio.sleep(50)
        self.antispam.remove(user)

    async def on_message(self, message):
        if message.author.bot:
            return
        author = message.author.id
        try:
            if message.guild.id == 264445053596991498:
                return
        except:
            pass

        if not db.profiles.count({"user_id":author}):
            data = {
                'user_id':author,
                'messages':1,
                'xp':1,
                "max_xp":100,
                "coins":100,
                "diamonds":10,
                "level":1,
                "is_private":False,
                "description":"None"
            }
            return db.profiles.insert_one(data)


        if not author in self.antispam:
            db.profiles.update_one({"user_id":author}, {'$inc':{'xp':1}})
            self.antispam.append(author)
            self.bot.loop.create_task(self.antiSpam(author))

        db.profiles.update_one({"user_id":author}, {'$inc':{'messages':1}})

        for x in db.profiles.find({"user_id":author}):
            if x['xp'] >= x['max_xp']:
                db.profiles.update_one({"user_id":author}, {'$set':{'xp':1}})
                db.profiles.update_one({"user_id":author}, {'$inc':{'max_xp':200}})
                db.profiles.update_one({"user_id":author}, {'$inc':{'level':1}})


                coinreward = random.randint(100, 200) * x['level'] + 1 - 100
                diamondreward = random.randint(10, 20) * x['level'] + 1 - 10
                rewards = [f'<:gold:514791023671509003> {coinreward} Coins', f'<:diagay:515536803407593486> {diamondreward} Diamonds']
                rewards = "\n".join(rewards)
                db.profiles.update_one({"user_id":author}, {'$inc':{'coins':coinreward}})
                db.profiles.update_one({"user_id":author}, {'$inc':{'diamonds':diamondreward}})

                e = discord.Embed(title="Level Up!", description=f":clap: Congratulations {message.author.name} you have leveled up to level {x['level'] + 1}. :clap:\n\nHere are your awesome perks!\n{rewards}", color=color())
                footer(message.author, e)
                e.set_thumbnail(url=utils.gif['clap1'])
                await message.author.send(embed=e)

def setup(bot):
    bot.add_cog(Tracker(bot))
