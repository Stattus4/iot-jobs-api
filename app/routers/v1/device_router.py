# -*- coding: utf-8 -*-

from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends
from pymongo.asynchronous.database import AsyncDatabase

from ...repositories.device_repository import DeviceRepository
from ...schemas.device_schemas import DeviceCreateRequest, DeviceModel, DeviceResponse, DeviceSearchRequest, DeviceSearchResponse
from ...services.device_services import DeviceServices
from ...mongodb import MongoDB


async def get_device_services():
    global device_services

    if device_services is None:
        device_repository = await DeviceRepository.get_instance()
        device_services = DeviceServices(device_repository)

    return device_services


device_services: DeviceServices | None = None

router = APIRouter()


@router.get(
    path="/{imei}",
    response_model=DeviceResponse,
    response_model_exclude_none=True
)
async def get_device(
    imei: str,
    device_services: DeviceServices = Depends(get_device_services)
) -> DeviceResponse:
    device = await device_services.search_by_imei(imei=imei)

    return DeviceResponse(
        version="1",
        device=device
    )


@router.post(
    path="/",
    response_model=DeviceResponse,
    response_model_exclude_none=True
)
async def create_device(
    device: DeviceCreateRequest = Body(...),
    device_services: DeviceServices = Depends(get_device_services)
) -> DeviceResponse:
    device = await device_services.create(imei=device.imei)

    return DeviceResponse(
        version="1",
        device=device
    )


@router.post(
    path="/search",
    response_model=DeviceSearchResponse,
    response_model_exclude_none=True
)
async def search_devices(
    search: DeviceSearchRequest = Body(...),
    mongodb_database: AsyncDatabase = Depends(MongoDB.get_database)
) -> DeviceSearchResponse:
    collection = mongodb_database.get_collection("devices")

    return []
