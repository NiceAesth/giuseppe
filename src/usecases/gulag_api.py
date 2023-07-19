from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp
import orjson
from common import BASE_GIUSEPPE_API_URL
from common.helpers import add_param
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

    async def get_profile(self, **kwargs: Any) -> osu.User:
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
        add_param(params, kwargs, "id")
        add_param(params, kwargs, "username", "name")
        data = await self._request(
            "GET",
            f"{self._base_url}/get_player_info",
            params=params,
        )
        return osu.User.model_validate(data.get("player"))

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None
