# -*- coding: utf-8 -*-

import uuid
from dataclasses import dataclass

from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.requests import Request

from ..context import request_id_ctx


@dataclass
class RequestIdMiddleware:

    app: ASGIApp

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)

            return

        request = Request(
            scope=scope,
            receive=receive
        )

        request_id: str = request.headers.get(
            "X-Request-ID",
            str(uuid.uuid4())
        )

        token = request_id_ctx.set(request_id)

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = list(
                    message.get("headers", [])
                )

                headers.append(
                    (b"x-request-id", request_id.encode("utf-8"))
                )

                message["headers"] = headers

            await send(message)

        # try:
        #     await self.app(scope, receive, send_wrapper)

        # finally:
        #     request_id_ctx.reset(token)

        await self.app(scope, receive, send_wrapper)
