# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from typing import Any

from ..repositories.device_repository import DeviceRepository
from ..models.device_models import DeviceCreateRequest, DeviceModel, DeviceSearchRequest


class DeviceServices:
    _device_repository: DeviceRepository

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    async def create_device(self, device_create_request: DeviceCreateRequest) -> DeviceModel:
        now = datetime.now(timezone.utc)

        device = {
            "imei": device_create_request.imei,
            "createdAt": now,
            "updatedAt": now,
            "lastSeenAt": None,
            "jobQueue": []
        }

        await self._device_repository.insert_one(
            document=device
        )

        return DeviceModel(**device)

    async def delete_device(self, imei: str) -> bool:
        delete_filter = {
            "imei": imei
        }

        return await self._device_repository.delete_one(
            delete_filter=delete_filter
        )

    async def search_device(self, device_search_request: DeviceSearchRequest) -> list[DeviceModel]:
        search_filter = device_search_request.filter

        find_filter: dict[str, Any] = {}

        if search_filter.imei is not None:
            if search_filter.imei.in_ is not None:
                find_filter["imei"] = {"$in": search_filter.imei.in_}

        if search_filter.createdAt is not None:
            if search_filter.createdAt.gte is not None and search_filter.createdAt.lte is not None:
                find_filter["createdAt"] = {
                    "$gte": search_filter.createdAt.gte,
                    "$lte": search_filter.createdAt.lte
                }

        if search_filter.updatedAt is not None:
            if search_filter.updatedAt.gte is not None and search_filter.updatedAt.lte is not None:
                find_filter["updatedAt"] = {
                    "$gte": search_filter.updatedAt.gte,
                    "$lte": search_filter.updatedAt.lte
                }

        if search_filter.lastSeenAt is not None:
            if search_filter.lastSeenAt.isEmpty is not None:
                find_filter["lastSeenAt"] = None if search_filter.lastSeenAt.isEmpty else {"$ne": None}  # noqa

            elif search_filter.lastSeenAt.gte is not None and search_filter.lastSeenAt.lte is not None:
                find_filter["lastSeenAt"] = {
                    "$gte": search_filter.lastSeenAt.gte,
                    "$lte": search_filter.lastSeenAt.lte
                }

        if search_filter.jobQueue is not None:
            if search_filter.jobQueue.isEmpty is not None:
                find_filter["jobQueue"] = {"$size": 0} if search_filter.jobQueue.isEmpty else {"$ne": []}  # noqa

            elif search_filter.jobQueue.containsAny is not None:
                find_filter["jobQueue"] = {
                    "$in": search_filter.jobQueue.containsAny
                }

        documents = await self._device_repository.find(
            find_filter=find_filter
        )

        return [DeviceModel(**document) for document in documents]

    async def search_device_by_imei(self, imei: str) -> DeviceModel | None:
        find_filter = {
            "imei": imei
        }

        device = await self._device_repository.find_one(
            find_filter=find_filter
        )

        if device is not None:
            return DeviceModel(**device)

        return None
