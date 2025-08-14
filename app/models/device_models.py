# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


# Model


class DeviceModel(BaseModel):
    imei: str = Field(default=..., min_length=15, max_length=15)
    createdAt: datetime
    updatedAt: datetime | None = None
    lastSeenAt: datetime | None = None
    jobQueue: list[str] | None = None


# DeviceSearchFilter


class ImeiFilter(BaseModel):
    in_: Annotated[list[str] | None, Field(alias="in", min_items=1)] = None


class DateRangeFilter(BaseModel):
    gte: datetime | None = None
    lte: datetime | None = None


class LastSeenAtFilter(BaseModel):
    isEmpty: bool | None = None
    gte: datetime | None = None
    lte: datetime | None = None


class JobQueueFilter(BaseModel):
    isEmpty: bool | None = None
    containsAny: list[str] | None = None


class DeviceSearchFilter(BaseModel):
    imei: ImeiFilter | None = None
    createdAt: DateRangeFilter | None = None
    updatedAt: DateRangeFilter | None = None
    lastSeenAt: LastSeenAtFilter | None = None
    jobQueue: JobQueueFilter | None = None


# Request / Response


class DeviceResponse(BaseModel):
    version: str
    device: DeviceModel | None


class DeviceCreateRequest(BaseModel):
    imei: str = Field(default=..., min_length=15, max_length=15)


class DeviceSearchRequest(BaseModel):
    filter: DeviceSearchFilter | None = None


class DeviceSearchResponse(BaseModel):
    version: str
    devices: list[DeviceModel] = Field(default_factory=list)
