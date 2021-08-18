from os import name
from asyncio import sleep
from discord import Intents,  Webhook, AsyncWebhookAdapter, Embed, webhook
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
import requests
import aiohttp
from discord.ext.commands import CommandNotFound, when_mentioned_or
from ..db import db
from glob import glob
from discord.utils import find


# PREFIX = "$"
OWNER_IDS = [701561771529470074]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
DATA_WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/876585742904721428/tXuHseUtA-5wz-HoN3ulv9LGxBq1tLYTIoe9PqDGahbSkKu9jllgOXen3Ac8cnsih0Jv"


def get_prefix(bot, message):
    prefix = db.feild("SELECT Prefix FROM guilds WHERE GuildID = ?" , message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def run_bot(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"[COGS] > [StegoBranch] > {cog} Cog Ready.")

    def all_ready(self):
        # return all([getattr(self, cog) for cog in COGS])
        pass


class Bot(BotBase): 
    def __init__(self):
        # Req self inits
        self.PREFIX = get_prefix
        self.scheduler = AsyncIOScheduler()
        self.ready = False
        self.cogs_ready = Ready()

        # Start DB autosave
        db.autosave(self.scheduler)

        # Intents - Members
        intents = Intents()
        intents.members = True

        super().__init__(command_prefix="$", owner_ids=OWNER_IDS)


    def setup(self):
        # Load cogs
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"[COGS] > [StegoBranch] > Loaded {cog} Cog.")

        print(f"[COGS] > [StegoBranch] > Loaded all Cogs.")


    # on_start
    # ------------
    # Extra self init -> sets self.ready to True -> outputs to console
    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()
            self.logchannel = self.get_channel(876585716136693790)


            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print(f"[STARTUP] > [StegoBranch] > Ready (Build No: {self.VERSION})")

        else:
            print("[API] > [StegoBranch] > Reconnected to the Discord API Gateway")
    

    # run -> nuns the bot
    def run(self, version):
        self.VERSION = version

        # Start setup
        print(f"[STARTUP] > [StegoBranch] > Running Setup...")
        print(f"[MISC] > [StegoBranch] > Prefix > {self.PREFIX}")
        self.setup()


        # Open token
        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

            print(f"[STARTUP] > [StegoBranch] > Running Bot (Build No: {self.VERSION})")
            
            # Run Bot
            super().run(self.TOKEN, reconnect=True)


    # Events Handlers
    # --------------
    # on_guild_join
    async def on_guild_join(self, guild):
        # Add to GuildDB
        print(guild.id)
        db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", "$", guild.id)
        print("new guild")


    # on_connect --> prints to console
    async def on_connect(self):
        print("[API] > [StegoBranch] > Connected to Discord API Gateway")


    # on_disconnect --> prints to console
    async def on_disconnect(self):
        print("[API] > [StegoBranch] > Disconnected from the Discord API Gateway")


    # on_error --> check if command_error -> true -> let user know -> else -> raise error
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            embed = Embed(title=f"Ah, slight problem!", description="Something went wrong on my end. I'll let the devs know.")
            await args[0].send(embed=embed)

        raise 


    # on_command_error --> checks type -> outputs to console
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
           pass
        elif hasattr(exc, "original"):
            raise exc.original 
        else:
            raise exc


    async def on_message(self, message):
        if message.author.bot: return
        await self.process_commands(message)


bot = Bot()