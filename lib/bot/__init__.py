from asyncio import sleep
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents
from discord.ext.commands import Bot as BotBase

PREFIX = "-"
OWNER_IDS = []
COGS = [path.split("\\")[-1][:-3] for path in glob("lib/cogs/*.py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.VERSION = None
        self.TOKEN = None
        self.stdout = None
        self.welcome = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all()
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
        print("setup complete")

    def run(self, version):
        self.VERSION = version
        self.setup()
        with open("lib/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, event_method, *args, **kwargs):
        if event_method == "on_command_error":
            await args[0].send("Something went wrong.")
        await self.stdout.send("An error occurred.")
        raise

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(816486491941109791)
            self.stdout = self.get_channel(824689618334384138


                                           )
            self.welcome = self.get_channel(816491731503546368)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            await self.stdout.send("Now online")
            self.ready = True
            print("bot ready")
        else:
            print("bot reconnected")

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_member_join(self, member):
        pass


bot = Bot()