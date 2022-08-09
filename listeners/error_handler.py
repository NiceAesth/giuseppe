import discord
from discord.ext import commands

class CommandErrorHandler(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error) -> None:
        if hasattr(ctx.command, "on_error"):
            return
        ignored = (commands.CommandNotFound)
        error = getattr(error, "original", error)
        if isinstance(error, ignored):
            return

        elif isinstance(error, discord.errors.Forbidden):
            return await ctx.send(
                f"I do not have permissions to perform ``{ctx.command}``!"
            )

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"``{ctx.command}`` has been disabled.")

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(
                f"You do not have the required permission for ``{ctx.command}``."
            )

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(
                f"Slow down! You are on a {error.retry_after:.2f}s cooldown."
            )

        elif isinstance(error, commands.BadArgument):
            return await ctx.send(
                f"You have specified an invalid argument or flag combo."
            )

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandErrorHandler(bot))