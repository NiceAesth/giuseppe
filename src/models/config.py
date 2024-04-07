from __future__ import annotations

import logging

import orjson
from pydantic import Field

from models.base import FrozenModel

logger = logging.getLogger("discord")


class MongoConfig(FrozenModel):
    host: str = "db:27017"
    database: str = "giuseppe"
    timeout: int = 1000


class Config(FrozenModel):
    log_level: str = "INFO"
    prefix: str = ","
    token: str = ""
    owners: list[int] = Field(default_factory=list)
    mongo: MongoConfig = MongoConfig()

    @classmethod
    def _create_config(cls) -> None:
        with open("config.json", "a+") as config_file:
            base_config = cls().model_dump()
            base_config_json = orjson.dumps(
                base_config,
                option=orjson.OPT_INDENT_2,
            ).decode()
            config_file.write(base_config_json)
            logger.warning(
                "A config file was not found! Please edit the newly created `config.json` and run again.",
            )

    @classmethod
    def get_config(cls) -> Config:
        try:
            config = cls.model_validate_file("config.json")
            return config
        except FileNotFoundError:
            cls._create_config()
            exit(1)
