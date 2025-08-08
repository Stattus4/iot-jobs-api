# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ImeiFilter(BaseModel):
    in_: Annotated[list[str] | None, Field(alias="in", min_items=1)] = None


class DateRangeFilter(BaseModel):
    gte: datetime | None = None
    lte: datetime | None = None


class JobQueueFilter(BaseModel):
    isEmpty: bool | None = None
    containsAny: list[str] | None = None


class DeviceSearchFilter(BaseModel):
    imei: ImeiFilter | None = None
    lastSeenAt: DateRangeFilter | None = None
    jobQueue: JobQueueFilter | None = None


class DeviceModel(BaseModel):
    imei: str = Field(..., min_length=15, max_length=15)
    createdAt: datetime
    lastSeenAt: datetime | None = None
    jobQueue: list[str] | None = None


class DeviceResponse(BaseModel):
    version: str
    device: DeviceModel | None


class DeviceCreateRequest(BaseModel):
    imei: str = Field(..., min_length=15, max_length=15)


class DeviceSearchRequest(BaseModel):
    filter: DeviceSearchFilter | None = None


class DeviceSearchResponse(BaseModel):
    version: str
    devices: list[DeviceModel] = Field(default_factory=list)
