import logging
from dataclasses import dataclass
from dataclasses_json import dataclass_json

logger = logging.getLogger('discord')

@dataclass_json
@dataclass(frozen=True)
class Config:
    log_level: str = 'WARNING'
    prefix: str = ','
    token: str = ''

    @classmethod
    def get_config(cls) -> 'Config':
        with open('config.json', 'a+') as config_file:
            config_file.seek(0)
            data = config_file.read()
            if data:
                config_file.close()
                return cls.from_json(data)
            fmt = cls().to_json()
            config_file.write(fmt)
            logger.warn("A config file was not found! Please edit the newly created `config.json` and run again.")
            config_file.close()
            exit()
