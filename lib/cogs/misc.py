from discord.ext.commands import Cog, command, has_permissions
from discord import Embed
from ..db import db

class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='ping', aliases=['latency'])
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @command(name='setprefix', hidden=True)
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            embed = Embed(title=f"Ah, slight problem!", description="Prefixes can't be more than 5 letters.")
            await ctx.send(embed=embed)
        else:
            db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            embed = Embed(title=f"Done!", description="Prefix set to `{new}`.")
            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")
        # print(f"[COGS] > [STEGOBRANCH] > Misc Cog Ready.")

def setup(bot):
    bot.add_cog(Misc(bot))