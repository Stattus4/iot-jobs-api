# -*- coding: utf-8 -*-

from ...models.error_models import ErrorResponse


class ErrorResponseBuilder:

    @staticmethod
    def build(message: str, request_id: str) -> ErrorResponse:
        return ErrorResponse(
            error={
                "message": message,
                "request_id": request_id,
            }
        )
