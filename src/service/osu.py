from __future__ import annotations

from repository.osu import OsuRepository


class OsuService:
    """Service for osu! user data."""

    def __init__(self, repository: OsuRepository) -> None:
        self.repository = repository

    async def exists(self, discord_id: int) -> bool:
        """Check if user exists in database.

        Args:
            discord_id (int): Discord ID.
        Returns:
            bool: True if user exists, False otherwise.
        """
        return await self.repository.exists(discord_id)

    async def get(self, discord_id: int) -> str:
        """Get osu! username from database.

        Args:
            discord_id (int): Discord ID.
        Raises:
            ValueError: User not found.
        Returns:
            str: osu! username.
        """
        return await self.repository.get(discord_id)

    async def add(self, discord_id: int, username: str) -> None:
        """Add / update osu! username to database.

        Args:
            discord_id (int): Discord ID.
            username (str): osu! username.
        """
        await self.repository.add(discord_id, username)

    async def delete(self, discord_id: int) -> None:
        """Delete osu! username from database.

        Args:
            discord_id (int): Discord ID.
        """
        await self.repository.delete(discord_id)
