from __future__ import annotations

from discord import Embed
from models.osu import User


class ProfileEmbed(Embed):
    def __init__(self, user: User, mode: int, **kwargs):
        super().__init__(
            title=f"osu!{mode!r} Profile for {user.info.name}",
            url=user.info.profile_url,
            description="",
            **kwargs,
        )

        self.set_thumbnail(url=user.info.avatar_url)
        self.description += (
            f"{user.stats.get(mode).pp}pp (#{user.stats.get(mode).rank})"
        )
