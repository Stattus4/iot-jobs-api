# -*- coding: utf-8 -*-

from typing import Literal

from pydantic import BaseModel


class PostCollectionsRequest(BaseModel):
    collection_name: str


class PostCollectionsIndexRequest(BaseModel):
    key: dict[str, Literal["ASCENDING", "DESCENDING"]]
    unique: bool


class PutCollectionsValidatorRequest(BaseModel):
    validator: dict
    validation_level: Literal["off", "strict", "moderate"] = "strict"
    validation_action: Literal["error", "warn"] = "error"
