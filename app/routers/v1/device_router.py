# -*- coding: utf-8 -*-

import logging

from fastapi import APIRouter, Body, Depends, HTTPException, status

from ...repositories.device_repository import DeviceRepository
from ...models.device_models import DeviceCreateRequest, DeviceResponse, DeviceSearchRequest, DeviceSearchResponse
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


@router.delete(
    path="/{imei}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_device(
    imei: str,
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> None:
    try:
        deleted = await device_services.delete_device(imei=imei)

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


@router.get(
    path="/{imei}",
    response_model=DeviceResponse,
    response_model_exclude_none=True
)
async def get_device(
    imei: str,
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> DeviceResponse:
    try:
        device = await device_services.search_device_by_imei(imei=imei)

        if device is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        return DeviceResponse(
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


@router.post(
    path="/",
    response_model=DeviceResponse,
    response_model_exclude_none=True
)
async def create_device(
    device_create_request: DeviceCreateRequest = Body(default=...),
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> DeviceResponse:
    try:
        device = await device_services.create_device(
            device_create_request=device_create_request
        )

        return DeviceResponse(
            version="v1",
            device=device
        )

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post(
    path="/search",
    response_model=DeviceSearchResponse,
    response_model_exclude_none=True
)
async def search_devices(
    device_search_request: DeviceSearchRequest = Body(default=...),
    device_services: DeviceServices = Depends(dependency=get_device_services)
) -> DeviceSearchResponse:
    try:
        devices = await device_services.search_device(
            device_search_request=device_search_request
        )

        return DeviceSearchResponse(
            version="v1",
            devices=devices
        )

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
