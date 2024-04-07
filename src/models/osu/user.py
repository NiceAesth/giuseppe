from __future__ import annotations

from emojiflags.lookup import lookup as flag_lookup  # type: ignore
from pydantic import computed_field

from ..base import FrozenModel

__all__ = ("User", "UserInfo", "UserStats")


class UserInfo(FrozenModel):
    id: int
    name: str
    safe_name: str
    priv: int
    clan_id: int
    country: str
    silence_end: int
    donor_end: int

    @computed_field  # type: ignore
    @property
    def profile_url(self) -> str:
        return f"{BASE_GIUSEPPE_URL}/u/{self.id}"

    @computed_field  # type: ignore
    @property
    def avatar_url(self) -> str:
        return f"{BASE_GIUSEPPE_AVATAR_URL}/{self.id}"

    @computed_field  # type: ignore
    @property
    def country_flag_emoji(self) -> str:
        return flag_lookup(self.country.upper())


class UserStats(FrozenModel):
    tscore: int
    rscore: int
    pp: int
    plays: int
    playtime: int
    acc: float
    max_combo: int
    xh_count: int
    x_count: int
    sh_count: int
    s_count: int
    a_count: int
    rank: int
    country_rank: int


class User(FrozenModel):
    info: UserInfo
    stats: dict[int, UserStats]
