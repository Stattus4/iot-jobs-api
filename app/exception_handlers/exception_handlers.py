# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(Exception)
    async def exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "detail": type(exc).__name__
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
