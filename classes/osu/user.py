from typing import Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass(frozen=True)
class UserInfo:
    id: int
    name: str
    safe_name: str
    priv: int
    clan_id: int
    country: str
    silence_end: int
    donor_end: int

@dataclass_json
@dataclass(frozen=True)
class UserStats:
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
    s_count:int
    a_count: int
    rank: int
    country_rank: int

@dataclass_json
@dataclass(frozen=True)
class User:
    info: UserInfo
    stats: Dict[int, UserStats]