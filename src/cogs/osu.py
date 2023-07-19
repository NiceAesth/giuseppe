from __future__ import annotations

from classes.bot import Giuseppe
from discord.ext import commands
from models import osu
from ui.embeds import ProfileEmbed
from ui.embeds import ScoreMultipleEmbed
from ui.embeds import ScoreSingleEmbed


class OsuCog(commands.Cog):
    def __init__(self, bot: Giuseppe) -> None:
        self.bot: Giuseppe = bot
        self.gulag_client = bot.gulag_client

    @commands.hybrid_command(name="link")
    async def link_command(self, ctx: commands.Context, name: str) -> None:
        profile = await self.gulag_client.get_user(username=name)
        await self.bot.osu_service.add(ctx.author.id, profile.info.name)
        await ctx.send(
            f"Your profile has been linked to **{profile.info.name}**.",
            delete_after=10,
        )

    @commands.hybrid_command(name="unlink")
    async def unlink_command(self, ctx: commands.Context) -> None:
        if not await self.bot.osu_service.exists(ctx.author.id):
            await ctx.send("You haven't linked your profile yet.", delete_after=10)
            return
        await self.bot.osu_service.delete(ctx.author.id)
        await ctx.send("Your profile has been unlinked.", delete_after=10)

    @commands.hybrid_command(name="profile", aliases=["p"])
    async def profile_command(
        self,
        ctx: commands.Context,
        name: str = None,
        mode: osu.Mode = osu.Mode.VANILLA_OSU,
    ) -> None:
        if name is None:
            name = await self.bot.osu_service.get(ctx.author.id)
        profile = await self.gulag_client.get_user(username=name)
        await ctx.send(embed=ProfileEmbed(profile, mode))

    @commands.hybrid_command(name="recent", aliases=["rs", "r"])
    async def recent_command(
        self,
        ctx: commands.Context,
        name: str = None,
        mode: osu.Mode = osu.Mode.VANILLA_OSU,
    ) -> None:
        if name is None:
            name = await self.bot.osu_service.get(ctx.author.id)
        profile = await self.gulag_client.get_user(username=name)
        score = (await self.gulag_client.get_user_recent(id=profile.info.id, limit=1))[
            0
        ]
        await ctx.send(embed=ScoreSingleEmbed(profile, mode, score))

    @commands.hybrid_command(name="top")
    async def top_command(
        self,
        ctx: commands.Context,
        name: str = None,
        mode: osu.Mode = osu.Mode.VANILLA_OSU,
    ) -> None:
        if name is None:
            name = await self.bot.osu_service.get(ctx.author.id)
        profile = await self.gulag_client.get_user(username=name)
        scores = await self.gulag_client.get_user_best(id=profile.info.id, limit=3)
        await ctx.send(embed=ScoreMultipleEmbed(profile, mode, scores))


async def setup(bot: Giuseppe) -> None:
    await bot.add_cog(OsuCog(bot))
