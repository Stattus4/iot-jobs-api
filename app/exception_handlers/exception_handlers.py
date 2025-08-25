# -*- coding: utf-8 -*-

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from ..context import request_id_ctx
from .builders.error_response_builder import ErrorResponseBuilder


logger = logging.getLogger(name=__name__)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(Exception)
    async def exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        logger.error("Unhandled exception: %s", exc)

        error_response = ErrorResponseBuilder.build(
            message=type(exc).__name__,
            request_id=request_id_ctx.get()
        )

        return JSONResponse(
            content=error_response.model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers={
                "X-Request-ID": request_id_ctx.get()
            }
        )
