from __future__ import annotations

from common import humanizer
from discord import Embed
from models.osu import Mode
from models.osu import Score
from models.osu import User


def _score_to_desc_str(score: Score) -> str:
    desc = (
        f"[**{score.beatmap.title}** [{score.beatmap.version}]]({score.beatmap.url})\n"
    )
    desc += f"**{score.pp:.2f}pp** - **{score.acc:.2f}%**\n"
    desc += f"**Max Combo:** {score.max_combo}x\n"
    desc += f"**Mods:** {score.mods}\n"
    desc += f"**Rank:** {score.grade}\n"
    desc += f"<t:{score.play_time.timestamp():.0f}:R>"

    return desc


class ScoreSingleEmbed(Embed):
    def __init__(self, user: User, mode: Mode, score: Score, **kwargs):
        super().__init__(
            **kwargs,
        )
        self.set_author(
            name=f"Recent osu!{mode!r} play for {user.info.name}",
            icon_url=user.info.avatar_url,
            url=user.info.profile_url,
        )
        self.description = _score_to_desc_str(score)
        self.set_thumbnail(url=score.beatmap.cover_url)


class ScoreMultipleEmbed(Embed):
    def __init__(self, user: User, mode: Mode, scores: list[Score], **kwargs):
        super().__init__(
            title=f"Top osu!{mode!r} plays for {user.info.name}",
            url=user.info.profile_url,
            **kwargs,
        )
        self.set_author(
            name=f"Top osu!{mode!r} plays for {user.info.name}",
            icon_url=user.info.avatar_url,
            url=user.info.profile_url,
        )
        self.description = ""
        for idx, score in enumerate(scores):
            self.description += f"{idx+1}. {_score_to_desc_str(score)}\n\n"
        self.set_thumbnail(url=score.beatmap.cover_url)
