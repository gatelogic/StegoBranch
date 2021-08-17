from discord.ext.commands import Cog, command

class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='ping', aliases=['latency'])
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")
        # print(f"[COGS] > [STEGOBRANCH] > Misc Cog Ready.")

def setup(bot):
    bot.add_cog(Misc(bot))