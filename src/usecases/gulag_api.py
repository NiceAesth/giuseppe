from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp
import orjson

from common import BASE_GIUSEPPE_API_URL
from common.helpers import add_param
from common.helpers import from_list
from models import osu

if TYPE_CHECKING:
    from typing import Any


def get_content_type(content_type: str) -> str:
    """Returns the content type."""
    return content_type.split(";")[0]


class GulagError(Exception):
    """Base exception for Gulag API errors."""

    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class GulagClient:
    """Gulag API Client."""

    __slots__ = (
        "_session",
        "_base_url",
    )

    def __init__(self):
        self._base_url = BASE_GIUSEPPE_API_URL
        self._session: aiohttp.ClientSession | None = None

    async def _request(
        self,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if self._session is None:
            self._session = aiohttp.ClientSession()

        async with self._session.request(method, *args, **kwargs) as resp:
            body = await resp.read()
            content_type = get_content_type(resp.headers.get("content-type", ""))
            if resp.status != 200:
                raise GulagError(resp.status)
            if content_type == "application/json":
                return orjson.loads(body)

    async def get_user(self, **kwargs: Any) -> osu.User:
        r"""Gets a user's profile.

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *id* (``int``) --
                User ID
            * *username* (``str``) --
                Username

        :return: User profile
        :rtype: osu.User
        """
        params = {"scope": "all"}
        add_param(params, kwargs, "id", converter=int)
        add_param(params, kwargs, "username", "name", converter=str)
        data = await self._request(
            "GET",
            f"{self._base_url}/get_player_info",
            params=params,
        )
        return osu.User.model_validate(data.get("player"))

    async def _get_type_scores(
        self,
        request_type: str,
        **kwargs: Any,
    ) -> list[osu.Score]:
        params = {"scope": request_type}
        add_param(params, kwargs, "id", converter=int)
        add_param(params, kwargs, "username", "name", converter=str)
        add_param(params, kwargs, "mods", converter=str)
        add_param(params, kwargs, "mode", converter=int)
        add_param(params, kwargs, "limit", converter=int)
        add_param(params, kwargs, "include_loved", converter=int)
        add_param(params, kwargs, "include_failed", converter=int)
        data = await self._request(
            "GET",
            f"{self._base_url}/get_player_scores",
            params=params,
        )
        return from_list(osu.Score.model_validate, data.get("scores"))

    async def get_user_best(
        self,
        **kwargs: Any,
    ) -> list[osu.Score]:
        r"""Gets a user's best scores.

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *id* (``int``) --
                User ID
            * *username* (``str``) --
                Username
            * *mods* (``str``) --
                Mods
            * *mode* (``int``) --
                Mode
            * *limit* (``int``) --
                Limit
            * *include_loved* (``bool``) --
                Include loved: Default is ``False``
            * *include_failed* (``bool``) --
                Include failed: Default is ``True``

        :return: User best scores
        :rtype: list[osu.Score]
        """
        return await self._get_type_scores("best", **kwargs)

    async def get_user_recent(
        self,
        **kwargs: Any,
    ) -> list[osu.Score]:
        r"""Gets a user's recent scores.

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *id* (``int``) --
                User ID
            * *username* (``str``) --
                Username
            * *mods* (``str``) --
                Mods
            * *mode* (``int``) --
                Mode
            * *limit* (``int``) --
                Limit
            * *include_loved* (``bool``) --
                Include loved: Default is ``True``
            * *include_failed* (``bool``) --

        :return: User recent scores
        :rtype: list[osu.Score]
        """
        if "include_loved" not in kwargs:
            kwargs["include_loved"] = True
        return await self._get_type_scores("recent", **kwargs)

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None
