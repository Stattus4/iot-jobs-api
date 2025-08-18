# -*- coding: utf-8 -*-

import logging

from fastapi import APIRouter, Body, Depends, HTTPException, status

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


logger = logging.getLogger(name=__name__)

router = APIRouter()


@router.post(
    path="",
    response_model=DevicesResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Device",
    response_model_exclude_none=False
)
async def post_devices(
    post_devices_request: PostDevicesRequest = Body(default=...),
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> DevicesResponse:
    try:
        device = await device_services.create_device(
            post_devices_request=post_devices_request
        )

        if device is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT
            )

        return DevicesResponse(
            version="v1",
            device=device
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    path="/{imei}",
    response_model=DevicesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Device",
    response_model_exclude_none=False
)
async def get_devices(
    imei: str,
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> DevicesResponse:
    try:
        device = await device_services.search_device_by_imei(
            imei=imei
        )

        if device is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        return DevicesResponse(
            version="v1",
            device=device
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.delete(
    path="/{imei}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Device"
)
async def delete_devices(
    imei: str,
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> None:
    try:
        deleted = await device_services.delete_device(
            imei=imei
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
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
    try:
        devices = await device_services.search_device(
            post_devices_search_request=post_devices_search_request
        )

        return PostDevicesSearchResponse(
            version="v1",
            devices=devices
        )

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
