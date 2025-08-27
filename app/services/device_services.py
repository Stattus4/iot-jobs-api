# -*- coding: utf-8 -*-

from datetime import datetime, timezone

from ..errors.repository_errors import DeviceNotFoundError, DuplicateDeviceError
from ..errors.service_errors import DeviceAlreadyExistsError, DeviceDeletionError, DeviceDoesNotExistError
from ..models.device_models import DeviceModel, PostDevicesRequest, PostDevicesSearchRequest
from ..repositories.device_repository import DeviceRepository
from ..services.builders.device_search_filter_builder import DeviceSearchFilterBuilder


class DeviceServices:

    _device_repository: DeviceRepository

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    async def create_device(self, post_devices_request: PostDevicesRequest) -> DeviceModel:
        now = datetime.now(timezone.utc)

        document = {
            "imei": post_devices_request.imei,
            "created_at": now,
            "updated_at": now,
            "last_seen_at": None,
            "job_queue": []
        }

        try:
            inserted_document = await self._device_repository.insert_one(
                document=document
            )

            return DeviceModel(**inserted_document)

        except DuplicateDeviceError:
            raise DeviceAlreadyExistsError()

    async def delete_device(self, imei: str) -> None:
        find_filter = {
            "imei": imei
        }

        delete_filter = {
            "imei": imei,
            "job_queue": []
        }

        try:
            document = await self._device_repository.find_one(
                find_filter=find_filter
            )

            device = DeviceModel(**document)

            if len(device.job_queue) > 0:
                raise DeviceDeletionError()

            await self._device_repository.delete_one(
                delete_filter=delete_filter
            )

        except DeviceNotFoundError:
            raise DeviceDoesNotExistError()

    async def search_device(self, post_devices_search_request: PostDevicesSearchRequest) -> list[DeviceModel]:
        device_search_filter = post_devices_search_request.filter

        find_filter = DeviceSearchFilterBuilder.build(
            device_search_filter=device_search_filter
        )

        documents = await self._device_repository.find(
            find_filter=find_filter
        )

        return [DeviceModel(**document) for document in documents]

    async def search_device_by_imei(self, imei: str) -> DeviceModel:
        find_filter = {
            "imei": imei
        }

        try:
            document = await self._device_repository.find_one(
                find_filter=find_filter
            )

            return DeviceModel(**document)

        except DeviceNotFoundError:
            raise DeviceDoesNotExistError()
