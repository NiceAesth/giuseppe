from __future__ import annotations

from enum import IntEnum

from discord.ext import commands

GAMEMODE_REPR_LIST = (
    "std",
    "taiko",
    "catch",
    "mania",
    "rx!std",
    "rx!taiko",
    "rx!catch",
    "rx!mania",  # unused
    "ap!std",
    "ap!taiko",  # unused
    "ap!catch",  # unused
    "ap!mania",  # unused
)


class Mode(IntEnum):
    VANILLA_OSU = 0
    VANILLA_TAIKO = 1
    VANILLA_CATCH = 2
    VANILLA_MANIA = 3

    RELAX_OSU = 4
    RELAX_TAIKO = 5
    RELAX_CATCH = 6
    RELAX_MANIA = 7

    AUTOPILOT_OSU = 8
    AUTOPILOT_TAIKO = 9
    AUTOPILOT_CATCH = 10
    AUTOPILOT_MANIA = 11

    def __repr__(self) -> str:
        return GAMEMODE_REPR_LIST[self.value]

    @classmethod
    async def convert(cls, ctx, argument):
        if argument.isnumeric():
            return cls(int(argument))
        mode_id = GAMEMODE_REPR_LIST.index(argument)
        return cls(mode_id)
