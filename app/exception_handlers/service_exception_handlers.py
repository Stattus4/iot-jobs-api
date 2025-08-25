# -*- coding: utf-8 -*-

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from ..context import request_id_ctx
from ..errors.service_errors import DeviceAlreadyExistsError, DeviceDeletionError, DeviceDoesNotExistError
from .builders.error_response_builder import ErrorResponseBuilder


logger = logging.getLogger(name=__name__)


def register_service_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(DeviceAlreadyExistsError)
    async def device_already_exists_handler(
        request: Request,
        exc: DeviceAlreadyExistsError
    ) -> JSONResponse:
        logger.warning("%s", type(exc).__name__)

        error_response = ErrorResponseBuilder.build(
            message=type(exc).__name__,
            request_id=request_id_ctx.get()
        )

        return JSONResponse(
            content=error_response.model_dump(),
            status_code=status.HTTP_409_CONFLICT
        )

    @app.exception_handler(DeviceDeletionError)
    async def device_deletion_handler(
        request: Request,
        exc: DeviceDeletionError
    ) -> JSONResponse:
        logger.warning("%s", type(exc).__name__)

        error_response = ErrorResponseBuilder.build(
            message=type(exc).__name__,
            request_id=request_id_ctx.get()
        )

        return JSONResponse(
            content=error_response.model_dump(),
            status_code=status.HTTP_409_CONFLICT
        )

    @app.exception_handler(DeviceDoesNotExistError)
    async def device_does_not_exist_handler(
        request: Request,
        exc: DeviceDoesNotExistError
    ) -> JSONResponse:
        logger.warning("%s", type(exc).__name__)

        error_response = ErrorResponseBuilder.build(
            message=type(exc).__name__,
            request_id=request_id_ctx.get()
        )

        return JSONResponse(
            content=error_response.model_dump(),
            status_code=status.HTTP_404_NOT_FOUND
        )
