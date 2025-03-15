from typing import List

from pymongo.collection import Collection

from fastapi_app.dataclasses.analysis_result.analysis_result import (
    AnalysisResultData,
    CreateAnalysisResultRequestData,
)
from fastapi_app.settings.database import mongo_connection
from fastapi_app.utils.dataclasses import build_dataclass_from_model_instance

from .queries import ANALYSIS_RESULTS_COLLECTION


class AnalysisResultProvider:
    _instance = None
    collection: Collection

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnalysisResultProvider, cls).__new__(cls)
            cls._instance.collection = mongo_connection.get_collection(
                ANALYSIS_RESULTS_COLLECTION
            )
        return cls._instance

    def create(self, request: CreateAnalysisResultRequestData) -> AnalysisResultData:
        inserted = self.collection.insert_one(request.to_dict())
        return build_dataclass_from_model_instance(
            AnalysisResultData, request.to_dict(), _id=str(inserted.inserted_id)
        )

    def get_latest_results(self, limit: int = 10) -> List[AnalysisResultData]:
        results = self.collection.find().sort("created_at", -1).limit(limit)
        return [
            build_dataclass_from_model_instance(AnalysisResultData, res)
            for res in results
        ]
