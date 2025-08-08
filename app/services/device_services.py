# -*- coding: utf-8 -*-

from datetime import datetime, timezone

from ..repositories.device_repository import DeviceRepository
from ..schemas.device_schemas import DeviceSearchFilter


class DeviceServices:
    _repository: DeviceRepository

    def __init__(self, repository: DeviceRepository):
        self._repository = repository

    async def create(self, imei: str) -> dict:
        device = {
            "imei": imei,
            "createdAt": datetime.now(timezone.utc),
            "jobQueue": []
        }

        await self._repository.insert_one(document=device)

        return device

    async def search(self, search_filter: DeviceSearchFilter) -> list:
        return []

    async def search_by_imei(self, imei: str) -> dict:
        find_filter = {
            "imei": imei
        }

        return await self._repository.find_one(find_filter=find_filter)
