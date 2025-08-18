# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from typing import Any

from ..models.device_models import DeviceModel, PostDevicesRequest, PostDevicesSearchRequest
from ..repositories.device_repository import DeviceRepository


class DeviceServices:
    _device_repository: DeviceRepository

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    async def create_device(self, post_devices_request: PostDevicesRequest) -> DeviceModel | None:
        now = datetime.now(timezone.utc)

        device = {
            "imei": post_devices_request.imei,
            "created_at": now,
            "updated_at": now,
            "last_seen_at": None,
            "job_queue": []
        }

        created = await self._device_repository.insert_one(
            document=device
        )

        if not created:
            return None

        return DeviceModel(**device)

    async def delete_device(self, imei: str) -> bool:
        delete_filter = {
            "imei": imei
        }

        return await self._device_repository.delete_one(
            delete_filter=delete_filter
        )

    async def search_device(self, post_devices_search_request: PostDevicesSearchRequest) -> list[DeviceModel]:
        search_filter = post_devices_search_request.filter

        find_filter: dict[str, Any] = {}

        if search_filter.imei is not None:
            if search_filter.imei.in_ is not None:
                find_filter["imei"] = {"$in": search_filter.imei.in_}

        if search_filter.created_at is not None:
            if search_filter.created_at.gte is not None and search_filter.created_at.lte is not None:
                find_filter["created_at"] = {
                    "$gte": search_filter.created_at.gte,
                    "$lte": search_filter.created_at.lte
                }

        if search_filter.updated_at is not None:
            if search_filter.updated_at.gte is not None and search_filter.updated_at.lte is not None:
                find_filter["updated_at"] = {
                    "$gte": search_filter.updated_at.gte,
                    "$lte": search_filter.updated_at.lte
                }

        if search_filter.last_seen_at is not None:
            if search_filter.last_seen_at.is_empty is not None:
                find_filter["last_seen_at"] = None if search_filter.last_seen_at.is_empty else {"$ne": None}  # noqa

            elif search_filter.last_seen_at.gte is not None and search_filter.last_seen_at.lte is not None:
                find_filter["last_seen_at"] = {
                    "$gte": search_filter.last_seen_at.gte,
                    "$lte": search_filter.last_seen_at.lte
                }

        if search_filter.job_queue is not None:
            if search_filter.job_queue.is_empty is not None:
                find_filter["job_queue"] = {"$size": 0} if search_filter.job_queue.is_empty else {"$ne": []}  # noqa

            elif search_filter.job_queue.contains_any is not None:
                find_filter["job_queue"] = {
                    "$in": search_filter.job_queue.contains_any
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
