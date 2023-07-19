from __future__ import annotations

from classes.bot import Giuseppe
from discord.ext import commands
from models import osu
from ui.embeds import ProfileEmbed


class OsuCog(commands.Cog):
    def __init__(self, bot: Giuseppe) -> None:
        self.bot: Giuseppe = bot
        self.gulag_client = bot.gulag_client

    @commands.hybrid_command(name="link")
    async def link_command(self, ctx: commands.Context, name: str) -> None:
        profile = await self.gulag_client.get_profile(username=name)
        await ctx.send(
            f"Your profile has been linked to **{profile.info.name}**.",
            delete_after=10,
        )

    @commands.hybrid_command(name="profile")
    async def profile_command(
        self,
        ctx: commands.Context,
        name: str = None,
        mode: osu.Mode = osu.Mode.VANILLA_OSU,
    ) -> None:
        profile = await self.gulag_client.get_profile(username=name)
        await ctx.send(embed=ProfileEmbed(profile, mode))

    @commands.hybrid_command(name="recent")
    async def recent_command(
        self,
        ctx: commands.Context,
        name: str = None,
        mode: osu.Mode = osu.Mode.VANILLA_OSU,
    ) -> None:
        profile = await self.gulag_client.get_profile(username=name)
        await ctx.send(embed=ProfileEmbed(profile, mode))

    @commands.hybrid_command(name="top")
    async def top_command(
        self,
        ctx: commands.Context,
        name: str = None,
        mode: osu.Mode = osu.Mode.VANILLA_OSU,
    ) -> None:
        profile = await self.gulag_client.get_profile(username=name)
        await ctx.send(embed=ProfileEmbed(profile, mode))


async def setup(bot: Giuseppe) -> None:
    await bot.add_cog(OsuCog(bot))
