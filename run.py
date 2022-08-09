import os
import logging
from classes.bot import Giuseppe

logger = logging.getLogger('discord')
bot = Giuseppe()

def list_module(directory) -> "list[str]":
    return (f for f in os.listdir(directory) if f.endswith(".py"))

@bot.listen("on_ready")
async def on_ready() -> None:
    module_folders = ["cogs", "listeners"]
    for module in module_folders:
        for extension in list_module(module):
            name = f"{module}.{os.path.splitext(extension)[0]}"
            try:
                await bot.load_extension(name)
            except Exception as e:
                logging.error(f"Failed loading module {name} : {e}")

if __name__ == "__main__":
    bot.run(reconnect=True)