###
# Copyright (c) 2023 NiceAesth. All rights reserved.
###
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase


class UserNotFound(Exception):
    """Exception raised when user is not found."""

    pass


class OsuRepository:
    """Repository for osu! user data."""

    __slots__ = ("database",)

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.database = database

    async def exists(self, discord_id: int) -> bool:
        """Check if user exists in database.

        Args:
            discord_id (int): Discord ID.
        Returns:
            bool: True if user exists, False otherwise.
        """
        return await self.database.osu.count_documents({"discord_id": discord_id}) > 0

    async def get(self, discord_id: int) -> str:
        """Get osu! username from database.

        Args:
            discord_id (int): Discord ID.
        Raises:
            ValueError: User not found.
        Returns:
            str: osu! username.
        """
        user = await self.database.osu.find_one({"discord_id": discord_id})
        if user is None:
            raise UserNotFound("User not found.")
        return user["username"]

    async def add(self, discord_id: int, username: str) -> None:
        """Add / update osu! username to database.

        Args:
            discord_id (int): Discord ID.
            username (str): osu! username.
        """
        await self.database.osu.update_one(
            {"discord_id": discord_id},
            {"$set": {"username": username}},
            upsert=True,
        )

    async def delete(self, discord_id: int) -> None:
        """Delete osu! username from database.

        Args:
            discord_id (int): Discord ID.
        """
        await self.database.osu.delete_one({"discord_id": discord_id})
