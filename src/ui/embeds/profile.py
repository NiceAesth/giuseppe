from __future__ import annotations

from common import humanizer
from discord import Embed
from models.osu import Mode
from models.osu import User


class ProfileEmbed(Embed):
    def __init__(self, user: User, mode: Mode, **kwargs):
        super().__init__(
            title=f"osu!{mode!r} Profile for {user.info.name}",
            url=user.info.profile_url,
            description=f"{user.stats.get(mode).pp}pp ({self._format_rank(user, mode)})",
            **kwargs,
        )

        self.set_thumbnail(url=user.info.avatar_url)

        self.add_field(
            name="Playtime",
            value=humanizer.seconds_to_text(user.stats.get(mode).playtime),
            inline=True,
        )
        self.add_field(
            name="Playcount",
            value=humanizer.number(user.stats.get(mode).plays),
            inline=True,
        )

        self.add_field(name="", value="", inline=False)

        self.add_field(
            name="Accuracy",
            value=f"{user.stats.get(mode).acc:.2f}%",
            inline=True,
        )
        self.add_field(
            name="Total Score",
            value=humanizer.number(user.stats.get(mode).tscore),
            inline=True,
        )

    @staticmethod
    def _format_rank(user: User, mode: int) -> str:
        return f"#{user.stats.get(mode).rank} | {user.info.country_flag_emoji} #{user.stats.get(mode).country_rank}"
