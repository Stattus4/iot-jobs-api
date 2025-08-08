# -*- coding: utf-8 -*-

from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends
from pymongo.asynchronous.database import AsyncDatabase

from ...schemas.devices import DeviceCreateRequest, DeviceModel, DeviceResponse, DeviceSearchRequest, DeviceSearchResponse
from ...mongodb import MongoDB


router = APIRouter()


@router.get(
    path="/{imei}",
    response_model=DeviceResponse,
    response_model_exclude_none=True
)
async def get_device(
    imei: str,
    mongodb_database: AsyncDatabase = Depends(MongoDB.get_database)
) -> DeviceResponse:
    collection = mongodb_database.get_collection("devices")

    document = await collection.find_one(
        filter={
            "imei": imei
        }
    )

    return DeviceResponse(
        version="1",
        device=document
    )


@router.post(
    path="/",
    response_model=DeviceResponse,
    response_model_exclude_none=True
)
async def create_device(
    device: DeviceCreateRequest = Body(...),
    mongodb_database: AsyncDatabase = Depends(MongoDB.get_database)
) -> DeviceResponse:
    device_dict = {
        "imei": device.imei,
        "createdAt": datetime.now(timezone.utc),
        "jobQueue": []
    }

    collection = mongodb_database.get_collection("devices")

    await collection.insert_one(device_dict)

    return DeviceResponse(
        version="1",
        device=device_dict
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
