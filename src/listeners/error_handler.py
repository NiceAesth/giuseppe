###
# Copyright (c) 2023 NiceAesth. All rights reserved.
###
from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from common.logging import logger
from discord.ext import commands
from usecases.gulag_api import GulagError


if TYPE_CHECKING:
    from classes.bot import Giuseppe
    from typing import Callable


class CommandErrorHandler(commands.Cog):
    """Handles any errors that may occur."""

    __slots__ = ("bot",)

    def __init__(self, bot: Giuseppe) -> None:
        self.bot = bot

        @bot.tree.error
        async def on_app_command_error(
            interaction: discord.Interaction,
            error: Exception,
        ) -> None:
            await self.error_handler(
                send_message=interaction.response.send_message,
                command=interaction.command,
                error=error,
                is_slash=True,
            )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if not isinstance(error, commands.CommandOnCooldown):
            if ctx.command is not None:
                ctx.command.reset_cooldown(ctx)

        await self.error_handler(
            send_message=ctx.send,
            command=ctx.command,
            error=error,
            is_slash=False,
        )

        if hasattr(ctx, "transaction"):
            ctx.transaction.finish()

    async def error_handler(
        self,
        send_message: Callable,
        command: commands.Command,
        error: Exception,
        is_slash: bool,
    ) -> None:
        if hasattr(command, "on_error") and not is_slash:
            return

        while hasattr(error, "original"):
            error = error.original

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.BotMissingPermissions):
            await send_message(
                f"I am missing the following permissions: ``{', '.join(error.missing_permissions)}`` for ``{command}``.",
                delete_after=10,
            )
            return

        elif isinstance(error, commands.MissingPermissions):
            await send_message(
                f"You are missing the following permissions: ``{', '.join(error.missing_permissions)}`` for ``{command}``.",
                delete_after=10,
            )
            return

        elif isinstance(error, discord.errors.Forbidden):
            await send_message(
                f"I do not have permissions to perform ``{command}``!",
                delete_after=10,
            )
            return

        elif isinstance(error, commands.NotOwner):
            await send_message("You are not the owner of this bot.", delete_after=5)
            return

        elif isinstance(error, commands.DisabledCommand):
            await send_message(f"``{command}`` has been disabled.", delete_after=5)
            return

        elif isinstance(error, commands.CommandOnCooldown):
            await send_message(
                f"Slow down! You are on a {error.retry_after:.2f}s cooldown.",
                delete_after=max(error.retry_after, 1),
            )
            return

        elif isinstance(error, commands.RangeError):
            await send_message(
                f"Value must be between **{error.minimum}** and **{error.maximum}**.",
                delete_after=10,
            )
            return

        elif isinstance(error, commands.UserInputError):
            await send_message(
                f"Invalid input for ``{command}``. Please check your input and try again.",
                delete_after=10,
            )
            return

        elif isinstance(error, GulagError):
            await send_message(
                f"The requested data could not be found.",
                delete_after=10,
            )
            return

        embed = discord.Embed(
            title="Oh no! An unexpected error has occured",
            color=discord.Color.red(),
        )
        embed.add_field(
            name="Error",
            value=f"```py\n{error}```",
        )
        embed.set_thumbnail(url="https://i.imgur.com/szL6ReL.png")
        await send_message(embed=embed)

        logger.exception(
            f"Ignoring exception in command {command}: ",
            exc_info=error,
        )


async def setup(bot: Giuseppe) -> None:
    await bot.add_cog(CommandErrorHandler(bot))
