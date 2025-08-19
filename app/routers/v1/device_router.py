# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, status

from ...errors.service_errors import DeviceAlreadyExistsError, DeviceDeletionError, DeviceDoesNotExistError
from ...models.device_models import DevicesResponse, PostDevicesRequest, PostDevicesSearchRequest, PostDevicesSearchResponse
from ...repositories.device_repository import DeviceRepository
from ...services.device_services import DeviceServices


async def get_device_services():
    if not hasattr(get_device_services, "_instance"):
        device_repository = await DeviceRepository.get_instance()

        get_device_services._instance = DeviceServices(
            device_repository=device_repository
        )

    return get_device_services._instance


router = APIRouter()


@router.post(
    path="",
    response_model=DevicesResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Device",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": DeviceAlreadyExistsError.__doc__
        }
    },
    response_model_exclude_none=False
)
async def post_devices(
    post_devices_request: PostDevicesRequest = Body(default=...),
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> DevicesResponse:
    device = await device_services.create_device(
        post_devices_request=post_devices_request
    )

    return DevicesResponse(
        version="v1",
        device=device
    )


@router.get(
    path="/{imei}",
    response_model=DevicesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Device",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": DeviceDoesNotExistError.__doc__
        }
    },
    response_model_exclude_none=False
)
async def get_devices(
    imei: str,
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> DevicesResponse:
    device = await device_services.search_device_by_imei(
        imei=imei
    )

    return DevicesResponse(
        version="v1",
        device=device
    )


@router.delete(
    path="/{imei}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Device",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": DeviceDoesNotExistError.__doc__
        },
        status.HTTP_409_CONFLICT: {
            "description": DeviceDeletionError.__doc__
        }
    }
)
async def delete_devices(
    imei: str,
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> None:
    await device_services.delete_device(
        imei=imei
    )


@router.post(
    path="/search",
    response_model=PostDevicesSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search Devices",
    response_model_exclude_none=False
)
async def post_devices_search(
    post_devices_search_request: PostDevicesSearchRequest = Body(default=...),
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> PostDevicesSearchResponse:
    devices = await device_services.search_device(
        post_devices_search_request=post_devices_search_request
    )

    return PostDevicesSearchResponse(
        version="v1",
        devices=devices
    )
