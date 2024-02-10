from __future__ import annotations

import time

from discord.ext import commands

from classes.bot import Giuseppe


class MiscCog(commands.Cog):
    def __init__(self, bot: Giuseppe) -> None:
        self.bot: Giuseppe = bot

    @commands.hybrid_command(name="ping")
    async def ping_command(self, ctx: commands.Context) -> None:
        t1 = time.perf_counter()
        msg = await ctx.send("🏓 Pong!")
        t2 = time.perf_counter()
        await msg.edit(content=f"🏓 Pong!: {(t2-t1)*1000:.2f}ms")


async def setup(bot: Giuseppe) -> None:
    await bot.add_cog(MiscCog(bot))
