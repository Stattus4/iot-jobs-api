# -*- coding: utf-8 -*-

import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from .exception_handlers.exception_handlers import register_exception_handlers
from .exception_handlers.service_exception_handlers import register_service_exception_handlers
from .logging_config import LoggingConfig
from .middlewares.request_id_middleware import RequestIdMiddleware
from .mongodb import MongoDB
from .routers import mongodb_router
from .routers.v1 import device_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await MongoDB.connect()

        logger.info("Connected to MongoDB")

    except Exception as e:
        logger.error("Failed to connect to MongoDB: %s", e)

    yield

    await MongoDB.close()

    logger.info("MongoDB connection closed")


LoggingConfig.config()

logger = logging.getLogger(name=__name__)

app = FastAPI(
    title="IoT Jobs API",
    lifespan=lifespan
)

register_exception_handlers(
    app=app
)

register_service_exception_handlers(
    app=app
)

app.add_middleware(
    middleware_class=RequestIdMiddleware
)

app.include_router(
    router=mongodb_router.router,
    prefix="/mongodb",
    tags=["mongodb"]
)

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(
    router=device_router.router,
    prefix="/devices",
    tags=["devices"]
)

app.include_router(router=v1_router)
