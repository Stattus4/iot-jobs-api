# -*- coding: utf-8 -*-

from typing import Any

from pymongo.asynchronous.collection import AsyncCollection
from pymongo.errors import DuplicateKeyError

from ..mongodb import MongoDB


class DeviceRepository():
    _collection: AsyncCollection

    def __init__(self, collection: AsyncCollection):
        self._collection = collection

    @classmethod
    async def get_instance(cls) -> "DeviceRepository":
        mongodb_database = await MongoDB.get_database()

        collection = mongodb_database.get_collection(
            name="devices"
        )

        return cls(collection)

    async def delete_one(self, delete_filter: dict) -> bool:
        delete_result = await self._collection.delete_one(
            filter=delete_filter
        )

        return delete_result.deleted_count == 1

    async def find(self, find_filter: dict) -> list[dict[str, Any]]:
        cursor = self._collection.find(
            filter=find_filter
        )

        return await cursor.to_list(length=None)

    async def find_one(self, find_filter: dict) -> dict[str, Any] | None:
        return await self._collection.find_one(
            filter=find_filter
        )

    async def insert_one(self, document: dict) -> bool:
        try:
            await self._collection.insert_one(
                document=document
            )

        except DuplicateKeyError:
            return False

        return True
