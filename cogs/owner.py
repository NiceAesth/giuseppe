import discord
from discord.ext import commands

class OwnerCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.is_owner()
    @commands.command(name="sync")
    async def sync_commands(self, ctx: commands.Context) -> None:
        await self.bot.tree.sync()
        await ctx.send("Syncing slash commands.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OwnerCog(bot))