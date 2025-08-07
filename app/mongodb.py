# -*- coding: utf-8 -*-

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.config import MONGODB_URI


class MongoDB:
    _client: AsyncMongoClient | None = None

    @classmethod
    async def close(cls) -> None:
        if cls._client is not None:
            await cls._client.close()

            cls._client = None

    @classmethod
    async def connect(cls) -> None:
        if cls._client is None:
            cls._client = AsyncMongoClient(MONGODB_URI)

            await cls._client.admin.command("ping")

    @classmethod
    async def get_database(cls) -> AsyncDatabase:
        if cls._client is None:
            raise RuntimeError()

        return cls._client.get_default_database()
