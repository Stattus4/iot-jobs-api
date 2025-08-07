# -*- coding: utf-8 -*-

from datetime import datetime

from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    imei: str = Field(..., min_length=15, max_length=15)


class DeviceResponse(DeviceCreate):
    createdAt: datetime
    lastSeenAt: datetime | None = None
    jobQueue: list[str] | None = None
