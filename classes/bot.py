from classes.config import Config
from discord import Intents
from discord.ext.commands import Bot
from classes.gulag_api import Gulag

class Giuseppe(Bot):
    def __init__(self, **kwargs) -> None:
        self.config = Config.get_config()
        self.gulag = Gulag()
        super().__init__(**kwargs,
            command_prefix=self.config.prefix,
            intents=Intents.all()
        )

    def run(self, **kwargs) -> None:
        super().run(self.config.token, log_level=self.config.log_level, **kwargs)