from __future__ import annotations

from classes.bot import Giuseppe
from discord.ext import commands


class OwnerCog(commands.Cog):
    def __init__(self, bot: Giuseppe) -> None:
        self.bot: Giuseppe = bot

    @commands.is_owner()
    @commands.command(name="sync")
    async def sync_commands(self, ctx: commands.Context) -> None:
        await self.bot.tree.sync()
        await ctx.send("Syncing slash commands.")


async def setup(bot: Giuseppe) -> None:
    await bot.add_cog(OwnerCog(bot))
