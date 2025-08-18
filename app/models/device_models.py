# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


# Model


class DeviceModel(BaseModel):

    imei: str = Field(default=..., min_length=15, max_length=15)
    created_at: datetime
    updated_at: datetime | None = None
    last_seen_at: datetime | None = None
    job_queue: list[str] | None = None


# DeviceSearchFilter


class ImeiFilter(BaseModel):

    in_: Annotated[list[str] | None, Field(alias="in", min_items=1)] = None


class DateRangeFilter(BaseModel):

    gte: datetime | None = None
    lte: datetime | None = None


class LastSeenAtFilter(BaseModel):

    is_empty: bool | None = None
    gte: datetime | None = None
    lte: datetime | None = None


class JobQueueFilter(BaseModel):

    is_empty: bool | None = None
    contains_any: list[str] | None = None


class DeviceSearchFilter(BaseModel):

    imei: ImeiFilter | None = None
    created_at: DateRangeFilter | None = None
    updated_at: DateRangeFilter | None = None
    last_seen_at: LastSeenAtFilter | None = None
    job_queue: JobQueueFilter | None = None


# Request / Response


class DevicesResponse(BaseModel):

    version: str
    device: DeviceModel | None


class PostDevicesRequest(BaseModel):

    imei: str = Field(default=..., min_length=15, max_length=15)


class PostDevicesSearchRequest(BaseModel):

    filter: DeviceSearchFilter | None = None


class PostDevicesSearchResponse(BaseModel):

    version: str
    devices: list[DeviceModel] = Field(default_factory=list)
