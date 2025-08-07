# -*- coding: utf-8 -*-

from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends
from pymongo.asynchronous.database import AsyncDatabase

from ..models.devices import DeviceCreate, DeviceResponse
from ..mongodb import MongoDB


router = APIRouter()


@router.get("/", response_model=list[DeviceResponse], response_model_exclude_none=True)
async def get_devices(
    mongodb_database: AsyncDatabase = Depends(MongoDB.get_database)
) -> list[DeviceResponse]:
    collection = mongodb_database.get_collection("devices")

    cursor = collection.find(
        filter={}
    )

    cursor_list = await cursor.to_list(length=None)

    return [DeviceResponse(**document) for document in cursor_list]


@router.post("/", response_model=DeviceResponse, response_model_exclude_none=True)
async def post_devices(
    device: DeviceCreate = Body(...),
    mongodb_database: AsyncDatabase = Depends(MongoDB.get_database)
) -> DeviceResponse:
    device_document = {
        "imei": device.imei,
        "createdAt": datetime.now(timezone.utc),
        "jobQueue": []
    }

    collection = mongodb_database.get_collection("devices")

    await collection.insert_one(device_document)

    return DeviceResponse(**device_document)
