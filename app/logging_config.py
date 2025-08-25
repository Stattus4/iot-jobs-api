# -*- coding: utf-8 -*-

import time
from logging import Filter, Formatter, getLogger, INFO, LogRecord, StreamHandler

from .context import request_id_ctx


class RequestIdFilter(Filter):

    def filter(self, record: LogRecord) -> bool:
        record.request_id = request_id_ctx.get()

        return True


class LoggingConfig:

    @staticmethod
    def config() -> None:
        formatter = Formatter(
            "%(asctime)s | %(levelname)s | %(request_id)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
        )

        formatter.converter = time.gmtime

        handler = StreamHandler()

        handler.addFilter(RequestIdFilter())
        handler.setFormatter(formatter)

        logger = getLogger()

        logger.setLevel(INFO)
        logger.addHandler(handler)
