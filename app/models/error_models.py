# -*- coding: utf-8 -*-

from pydantic import BaseModel


class ErrorModel(BaseModel):

    message: str
    request_id: str


class ErrorResponse(BaseModel):

    error: ErrorModel
