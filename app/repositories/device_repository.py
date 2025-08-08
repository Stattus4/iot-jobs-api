# -*- coding: utf-8 -*-

from pymongo.asynchronous.collection import AsyncCollection

from ..mongodb import MongoDB


class DeviceRepository():
    _collection: AsyncCollection

    def __init__(self, collection: AsyncCollection):
        self._collection = collection

    @classmethod
    async def get_instance(cls) -> "DeviceRepository":
        mongodb_database = await MongoDB.get_database()
        collection = mongodb_database.get_collection("devices")

        return cls(collection)

    async def find(self, find_filter: dict) -> list:
        cursor = self._collection.find(filter=find_filter)

        return await cursor.to_list()

    async def find_one(self, find_filter: dict) -> dict | None:
        return await self._collection.find_one(filter=find_filter)

    async def insert_one(self, document: dict) -> None:
        await self._collection.insert_one(document=document)
