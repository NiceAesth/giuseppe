from __future__ import annotations

from datetime import datetime

from models.base import FrozenModel
from models.osu.beatmap import Beatmap
from models.osu.mode import Mode
from models.osu.mods import Mods

__all__ = ("Score",)


class Score(FrozenModel):
    id: int
    play_time: datetime
    grade: str
    mods: Mods
    mode: Mode
    beatmap: Beatmap
    score: int
    pp: float
    acc: float
    max_combo: int
    status: int
    time_elapsed: int
    perfect: bool
    n300: int
    n100: int
    n50: int
    nmiss: int
    ngeki: int
    nkatu: int
