# -*- coding: utf-8 -*-

from typing import Any

from ...models.device_models import DeviceSearchFilter


class DeviceSearchFilterBuilder:

    @staticmethod
    def build(device_search_filter: DeviceSearchFilter) -> dict[str, Any]:
        find_filter: dict[str, Any] = {}

        if device_search_filter.imei is not None:
            if device_search_filter.imei.in_ is not None:
                find_filter["imei"] = {"$in": device_search_filter.imei.in_}

        if device_search_filter.created_at is not None:
            if device_search_filter.created_at.gte is not None and device_search_filter.created_at.lte is not None:
                find_filter["created_at"] = {
                    "$gte": device_search_filter.created_at.gte,
                    "$lte": device_search_filter.created_at.lte
                }

        if device_search_filter.updated_at is not None:
            if device_search_filter.updated_at.gte is not None and device_search_filter.updated_at.lte is not None:
                find_filter["updated_at"] = {
                    "$gte": device_search_filter.updated_at.gte,
                    "$lte": device_search_filter.updated_at.lte
                }

        if device_search_filter.last_seen_at is not None:
            if device_search_filter.last_seen_at.is_empty is not None:
                find_filter["last_seen_at"] = None if device_search_filter.last_seen_at.is_empty else {"$ne": None}  # noqa

            elif device_search_filter.last_seen_at.gte is not None and device_search_filter.last_seen_at.lte is not None:
                find_filter["last_seen_at"] = {
                    "$gte": device_search_filter.last_seen_at.gte,
                    "$lte": device_search_filter.last_seen_at.lte
                }

        if device_search_filter.job_queue is not None:
            if device_search_filter.job_queue.is_empty is not None:
                find_filter["job_queue"] = {"$size": 0} if device_search_filter.job_queue.is_empty else {"$ne": []}  # noqa

            elif device_search_filter.job_queue.contains_any is not None:
                find_filter["job_queue"] = {
                    "$in": device_search_filter.job_queue.contains_any
                }

        return find_filter
