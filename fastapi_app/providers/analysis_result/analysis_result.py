from typing import List

from pymongo.collection import Collection

from fastapi_app.dataclasses.analysis_result.analysis_result import AnalysisResultData
from fastapi_app.dataclasses.models_ia import IndividualCommentAnalysis
from fastapi_app.settings.database import mongo_connection
from fastapi_app.utils.dataclasses import build_dataclass_from_model_instance

from .queries import ANALYSIS_RESULTS_COLLECTION
import redis
from fastapi_app.settings.config import REDIS_HOST, REDIS_HOST_PORT


class AnalysisResultProvider:
    _instance = None
    collection: Collection
    redis_client: redis.Redis

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnalysisResultProvider, cls).__new__(cls)
            cls._instance.collection = mongo_connection.get_collection(
                ANALYSIS_RESULTS_COLLECTION
            )
            cls._instance.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_HOST_PORT,
                db=0,
                decode_responses=True,
            )

        return cls._instance

    def _get_redis_key(self, media_id: str) -> str:
        return f"analyzed:{media_id}"

    def is_recently_analyzed(self, media_id: str) -> bool:
        return self.redis_client.exists(self._get_redis_key(media_id)) > 0

    def mark_as_analyzed(self, media_id: str, expiration_seconds: int = 7200) -> None:
        self.redis_client.set(self._get_redis_key(media_id), "1", ex=expiration_seconds)

    def create(self, request: IndividualCommentAnalysis) -> AnalysisResultData:
        inserted = self.collection.insert_one(request.to_dict())
        return build_dataclass_from_model_instance(
            AnalysisResultData, request.to_dict(), _id=str(inserted.inserted_id)
        )

    def create_many_results(
        self, requests: List[IndividualCommentAnalysis]
    ) -> List[AnalysisResultData]:
        documents = [r.to_dict() for r in requests]
        result = self.collection.insert_many(documents)
        return [
            build_dataclass_from_model_instance(
                AnalysisResultData, doc, _id=str(inserted_id)
            )
            for doc, inserted_id in zip(documents, result.inserted_ids)
        ]

    def get_latest_results(self, limit: int = 10) -> List[AnalysisResultData]:
        results = self.collection.find().sort("created_at", -1).limit(limit)
        return [
            build_dataclass_from_model_instance(AnalysisResultData, res)
            for res in results
        ]
