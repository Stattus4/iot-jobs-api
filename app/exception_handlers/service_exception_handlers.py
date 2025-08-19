# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from ..errors.service_errors import DeviceAlreadyExistsError, DeviceDeletionError, DeviceDoesNotExistError


def register_service_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(DeviceAlreadyExistsError)
    async def device_already_exists_handler(
        request: Request,
        exc: DeviceAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "detail": type(exc).__name__
            },
            status_code=status.HTTP_409_CONFLICT
        )

    @app.exception_handler(DeviceDeletionError)
    async def device_deletion_handler(
        request: Request,
        exc: DeviceDeletionError
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "detail": type(exc).__name__
            },
            status_code=status.HTTP_409_CONFLICT
        )

    @app.exception_handler(DeviceDoesNotExistError)
    async def device_does_not_exist_handler(
        request: Request,
        exc: DeviceDoesNotExistError
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "detail": type(exc).__name__
            },
            status_code=status.HTTP_404_NOT_FOUND
        )
