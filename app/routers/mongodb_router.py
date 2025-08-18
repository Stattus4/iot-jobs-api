# -*- coding: utf-8 -*-

import logging
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status

from ..models.mongodb_models import PostCollectionsIndexRequest, PostCollectionsRequest, PutCollectionsValidatorRequest
from ..mongodb import MongoDB
from ..services.mongodb_services import MongoDBServices


async def get_mongodb_services():
    if not hasattr(get_mongodb_services, "_instance"):
        mongodb_database = await MongoDB.get_database()

        get_mongodb_services._instance = MongoDBServices(mongodb_database)

    return get_mongodb_services._instance


logger = logging.getLogger(name=__name__)

router = APIRouter()


@router.post(
    path="/collections",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    summary="Create Collection",
    response_model_exclude_none=False
)
async def post_collections(
    post_collections_request: PostCollectionsRequest,
    mongodb_services: MongoDBServices = Depends(
        dependency=get_mongodb_services
    )
) -> None:
    try:
        created = await mongodb_services.create_collection(
            post_collections_request=post_collections_request
        )

        if not created:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT
            )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.delete(
    path="/collections/{collection_name}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Collection",
    response_model_exclude_none=False
)
async def delete_collections(
    collection_name: str,
    mongodb_services: MongoDBServices = Depends(
        dependency=get_mongodb_services
    )
) -> None:
    try:
        await mongodb_services.delete_collection(
            collection_name=collection_name
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    path="/collections/{collection_name}/index",
    response_model=list[dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Get Collection Indexes",
    response_model_exclude_none=False
)
async def get_collections_index(
    collection_name: str,
    mongodb_services: MongoDBServices = Depends(
        dependency=get_mongodb_services
    )
) -> list[dict[str, Any]]:
    try:
        return await mongodb_services.get_collection_indexes(
            collection_name=collection_name
        )

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post(
    path="/collections/{collection_name}/index",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    summary="Create Collection Index",
    response_model_exclude_none=False
)
async def post_collections_index(
    collection_name: str,
    post_collections_index_request: PostCollectionsIndexRequest = Body(
        default=...
    ),
    mongodb_services: MongoDBServices = Depends(
        dependency=get_mongodb_services
    )
) -> None:
    try:
        created = await mongodb_services.create_collection_index(
            collection_name=collection_name,
            post_collections_index_request=post_collections_index_request
        )

        if not created:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT
            )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.delete(
    path="/collections/{collection_name}/index/{index_name}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Collection Index",
    response_model_exclude_none=False
)
async def delete_collections_index(
    collection_name: str,
    index_name: str,
    mongodb_services: MongoDBServices = Depends(
        dependency=get_mongodb_services
    )
) -> None:
    try:
        deleted = await mongodb_services.delete_collection_index(
            collection_name=collection_name,
            index_name=index_name
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    path="/collections/{collection_name}/validator",
    response_model=dict[str, Any] | None,
    status_code=status.HTTP_200_OK,
    summary="Get Collection Validator",
    response_model_exclude_none=False
)
async def get_collections_validator(
    collection_name: str,
    mongodb_services: MongoDBServices = Depends(
        dependency=get_mongodb_services
    )
) -> dict[str, Any] | None:
    try:
        return await mongodb_services.get_collection_validator(
            collection_name=collection_name
        )

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.put(
    path="/collections/{collection_name}/validator",
    response_model=None,
    status_code=status.HTTP_200_OK,
    summary="Update Collection Validator",
    response_model_exclude_none=False
)
async def put_collections_validator(
    collection_name: str,
    put_collections_validator_request: PutCollectionsValidatorRequest = Body(
        default=...
    ),
    mongodb_services: MongoDBServices = Depends(
        dependency=get_mongodb_services
    )
) -> None:
    try:
        await mongodb_services.update_collection_validator(
            collection_name=collection_name,
            put_collections_validator_request=put_collections_validator_request
        )

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    path="/collections/{collection_name}/validator/validation-error-summary",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get Collection Validator Validation Error Summary",
    response_model_exclude_none=False
)
async def get_collections_validator_validation_error_summary(
    collection_name: str,
    mongodb_services: MongoDBServices = Depends(
        dependency=get_mongodb_services
    )
) -> dict[str, Any]:
    try:
        validator = await mongodb_services.get_collection_validator(
            collection_name=collection_name
        )

        if validator is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        return await mongodb_services.get_collection_validator_validation_error_summary(
            collection_name=collection_name,
            validator=validator
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("%s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
