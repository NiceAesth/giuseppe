import discord
from discord.ext import commands
from classes import osu
from classes import embeds

class OsuCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="link")
    async def link_command(self, ctx: commands.Context, name: str) -> None:
        await ctx.send(f"Your profile has been linked to {name}")
    
    @commands.hybrid_command(name="profile")
    async def profile_command(self, ctx: commands.Context, name: str = None, mode: osu.Mode = osu.Mode.VANILLA_OSU) -> None:
        profile = await self.bot.gulag.get_profile(name)
        await ctx.send(embed=embeds.ProfileEmbed(profile, mode))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OsuCog(bot))