from __future__ import annotations

from datetime import datetime

from pydantic import computed_field

from ..base import FrozenModel
from .mode import Mode

__all__ = ("Beatmap",)


class Beatmap(FrozenModel):
    id: int
    set_id: int
    md5: str
    artist: str
    title: str
    version: str
    creator: str
    last_update: datetime
    total_length: int
    max_combo: int
    status: int
    plays: int
    passes: int
    mode: Mode
    bpm: float
    cs: float
    od: float
    ar: float
    hp: float
    diff: float

    @computed_field  # type: ignore
    @property
    def url(self) -> str:
        return f"https://osu.ppy.sh/b/{self.id}"

    @computed_field  # type: ignore
    @property
    def cover_url(self) -> str:
        return f"https://assets.ppy.sh/beatmaps/{self.set_id}/covers/list.jpg"
