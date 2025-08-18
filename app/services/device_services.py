# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from typing import Any

from ..models.device_models import DeviceModel, PostDevicesRequest, PostDevicesSearchRequest
from ..repositories.device_repository import DeviceRepository
from ..services.builders.device_search_filter_builder import DeviceSearchFilterBuilder


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
            "imei": imei,
            "job_queue": []
        }

        return await self._device_repository.delete_one(
            delete_filter=delete_filter
        )

    async def search_device(self, post_devices_search_request: PostDevicesSearchRequest) -> list[DeviceModel]:
        device_search_filter = post_devices_search_request.filter

        find_filter = DeviceSearchFilterBuilder.build(
            device_search_filter=device_search_filter
        )

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
