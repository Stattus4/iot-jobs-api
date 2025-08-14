# -*- coding: utf-8 -*-

import logging
import time
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

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


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
    level=logging.INFO
)

logging.Formatter.converter = time.gmtime

logger = logging.getLogger(name=__name__)

app = FastAPI(
    title="IoT Jobs API",
    lifespan=lifespan
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
