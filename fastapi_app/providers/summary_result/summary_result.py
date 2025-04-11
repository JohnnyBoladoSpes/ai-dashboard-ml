from pymongo.collection import Collection

from fastapi_app.settings.database import mongo_connection
from fastapi_app.dataclasses.models_ia import (
    SentimentAnalysisSummary,
    CreateSentimentSummaryData,
)
from fastapi_app.utils.dataclasses import build_dataclass_from_model_instance

from .queries import SUMMARY_RESULT_COLLECTION


class SummaryResultProvider:
    """Handles storage of sentiment analysis summaries in MongoDB."""

    _instance = None
    collection: Collection

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SummaryResultProvider, cls).__new__(cls)
            cls._instance.collection = mongo_connection.get_collection(
                SUMMARY_RESULT_COLLECTION
            )
        return cls._instance

    def create(self, request: CreateSentimentSummaryData) -> SentimentAnalysisSummary:
        """Insert a summary into the MongoDB collection."""
        inserted = self.collection.insert_one(request.to_dict())
        return build_dataclass_from_model_instance(
            SentimentAnalysisSummary, request.to_dict(), _id=str(inserted.inserted_id)
        )

    def get_summary_by_id(self, summary_id: str) -> dict:
        """Retrieve a summary by its ID."""
        return self.collection.find_one({"summary_id": summary_id})
