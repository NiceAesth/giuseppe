from __future__ import annotations

from cogs import LOAD_EXTENSIONS as COGS_LOAD
from common.logging import init_logging
from common.logging import logger
from discord import Intents
from discord import User
from discord.ext.commands import Bot
from listeners import LOAD_EXTENSIONS as LISTENER_LOAD
from models.config import Config
from usecases.gulag_api import GulagClient


async def _load_extensions(bot: Giuseppe):
    for cog in COGS_LOAD:
        await bot.load_extension(cog)
    for listener in LISTENER_LOAD:
        await bot.load_extension(listener)


class Giuseppe(Bot):
    """Giuseppe Bot"""

    __slots__ = (
        "config",
        "gulag_client",
    )

    def __init__(self, **kwargs) -> None:
        self.config = Config.get_config()
        super().__init__(
            **kwargs,
            command_prefix=self.config.prefix,
            intents=Intents.all(),
        )
        init_logging(self.config.log_level)
        self.gulag_client = GulagClient()

    def setup_services(self) -> None:
        logger.info("Setting up services...")

    async def setup_hook(self) -> None:
        logger.info("Setting up modules...")
        await self.load_extension("jishaku")
        await _load_extensions(self)

    async def on_ready(self) -> None:
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def is_owner(self, user: User) -> bool:
        if user.id in self.config.owners:
            return True
        return await super().is_owner(user)

    def run(self, **kwargs) -> None:
        super().run(self.config.token, log_handler=None, **kwargs)

    async def close(self) -> None:
        logger.info("Closing...")
        await self.gulag_client.close()
        await super().close()
