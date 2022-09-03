from __future__ import annotations

from discord import Embed

from classes.osu.user import User


class ProfileEmbed(Embed):
    def __init__(self, user: User, mode: int, **kwargs):
        super().__init__(
            title=f"osu!{mode!r} Profile for {user.info.name}",
            url=f"https://giuseppeosu.tk/u/{user.info.id}",
            description="",
            **kwargs,
        )

        self.set_thumbnail(url=f"https://a.giuseppeosu.tk/{user.info.id}")
        self.description += (
            f"{user.stats.get(mode).pp}pp (#{user.stats.get(mode).rank})"
        )
