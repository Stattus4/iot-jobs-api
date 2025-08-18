# -*- coding: utf-8 -*-

import json
from typing import Any

from bson import json_util
from jsonschema import validate, ValidationError
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import CollectionInvalid, OperationFailure

from ..models.mongodb_models import PostCollectionsIndexRequest, PostCollectionsRequest, PutCollectionsValidatorRequest
from ..mongodb import MongoDB


class MongoDBServices:

    _database: AsyncDatabase

    def __init__(self, database: AsyncDatabase):
        self._database = database

    async def create_collection(
        self,
        post_collections_request: PostCollectionsRequest
    ) -> bool:
        try:
            await self._database.create_collection(
                name=post_collections_request.collection_name
            )

        except CollectionInvalid:
            return False

        return True

    async def create_collection_index(
        self,
        collection_name: str,
        post_collections_index_request: PostCollectionsIndexRequest
    ) -> bool:
        order_map = {
            "ASCENDING": ASCENDING,
            "DESCENDING": DESCENDING
        }

        collection = self._database.get_collection(
            name=collection_name
        )

        keys = [
            (field, order_map[order]) for field, order in post_collections_index_request.key.items()
        ]

        try:
            await collection.create_index(
                keys=keys,
                unique=post_collections_index_request.unique
            )

        except OperationFailure:
            return False

        return True

    async def delete_collection(
        self,
        collection_name: str
    ) -> None:
        await self._database.drop_collection(
            name_or_collection=collection_name
        )

    async def delete_collection_index(
        self,
        collection_name: str,
        index_name: str
    ) -> bool:
        try:
            collection = self._database.get_collection(
                name=collection_name
            )

            await collection.drop_index(
                index_or_name=index_name
            )

        except OperationFailure:
            return False

        return True

    async def get_collection_indexes(
        self,
        collection_name: str
    ) -> list[dict[str, Any]]:
        collection = self._database.get_collection(
            name=collection_name
        )

        command_cursor = await collection.list_indexes()

        return [dict(i) for i in await command_cursor.to_list(length=None)]

    async def get_collection_validator(
        self,
        collection_name: str
    ) -> dict[str, Any] | None:
        result = await self._database.command(
            command="listCollections",
            filter={
                "name": collection_name
            }
        )

        cursor = result.get("cursor", {})
        first_batch = cursor.get("firstBatch", [])
        first_batch_0 = first_batch[0] if first_batch else {}
        options = first_batch_0.get("options", {})
        validator = options.get("validator", None)

        return validator

    async def get_collection_validator_validation_error_summary(
        self,
        collection_name: str,
        validator: dict[str, Any]
    ) -> dict[str, Any]:
        json_schema = validator.get("$jsonSchema", None)

        collection = self._database.get_collection(
            name=collection_name
        )

        cursor = collection.find()

        validation_error_documents = []

        for document in await cursor.to_list(length=None):
            try:
                validate(
                    instance=json.loads(
                        json_util.dumps(document)
                    ),
                    schema=json_schema
                )

            except ValidationError as e:
                validation_error_documents.append({
                    "_id": str(document["_id"]),
                    "validation_error_message": e.message
                })

        return {
            "collection_name": collection_name,
            "count_documents": await collection.count_documents(filter={}),
            "validation_error_count": len(validation_error_documents),
            "validation_error_documents": validation_error_documents
        }

    async def update_collection_validator(
        self,
        collection_name: str,
        put_collections_validator_request: PutCollectionsValidatorRequest
    ) -> None:
        options = {
            "validator": put_collections_validator_request.validator,
            "validationLevel": put_collections_validator_request.validation_level,
            "validationAction": put_collections_validator_request.validation_action
        }

        await self._database.command(
            command="collMod",
            value=collection_name,
            **options
        )
