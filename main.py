from imports import *

async def run():
    bot = LeEpic()
    await bot.start(config.bot_token)

class LeEpic(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=self._get_shagger_prefix)
        self.loop.create_task(self.load_modules())

    async def _get_shagger_prefix(self, bot, message):
        prefix = utils.prefix(message)
        return commands.when_mentioned_or(prefix)(bot, message)

    async def load_modules(self):
        await self.wait_until_ready()
        modules = [x.stem for x in Path('modules').glob('*.py')]
        for module in modules:
            try:
                self.load_extension(f'modules.{module}')
                print(f"Loaded {module}")
            except Exception as e:
                print(f"Failed to load {module} : {e}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            return await utils.error(ctx, "Bad Argument", str(error))

    async def on_command(self, ctx):
        if db.commands.count({"name":ctx.command.qualified_name}):
            req_points = [x['points'] for x in db.commands.find({"name":ctx.command.qualified_name})][0]
            if req_points != 0 and not await pointlessRaw(ctx):
                db.profiles.update_one({"user_id":ctx.author.id}, {'$inc':{'points':-req_points}})

    async def on_ready(self):
        print("Ok this is epic")

    async def on_message(self, message):
        Counters.messages_sent += 1
        if message.author.bot:
            return

        if message.content == "?server_prefix":
            await message.channel.send(f"The prefix for this server is : {prefix(message)}")

        await self.process_commands(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
