import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field


class AnalysisRequestModel(BaseModel):
    """Model for incoming analysis requests."""

    comment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = Field(..., description="Identifier of the user making the request")
    company_id: Optional[str] = Field(
        None, description="Company related to the request"
    )
    source: Optional[str] = Field(
        None, description="Data source (e.g., Instagram, Twitter, API)"
    )
    text: str = Field(...)
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnalysisResultModel(BaseModel):
    """Model for storing analysis results."""

    comment_id: str = Field(...)
    sentiment: str = Field(...)
    confidence: Optional[float] = None
    keywords: Optional[List[str]] = Field(
        default_factory=list, description="Extracted keywords"
    )
    topics: Optional[List[str]] = Field(
        default_factory=list, description="Identified topics"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserActivityModel(BaseModel):
    """Model to track user interactions with the AI API."""

    user_id: str = Field(...)
    comment_id: str = Field(...)
    endpoint: str = Field(...)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = Field(default="pending", description="Status of the request")


class EngagementMetricModel(BaseModel):
    """Model to store engagement metrics from social media posts."""

    post_id: str = Field(...)
    likes: int = Field(default=0)
    comments: int = Field(default=0)
    shares: int = Field(default=0)
    views: int = Field(default=0)
    saves: int = Field(default=0)
    clicks: int = Field(default=0)
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnalysisSummaryModel(BaseModel):
    """Model to store the summary of a sentiment analysis batch."""

    summary_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    total_comments: int = Field(..., description="Number of comments analyzed")
    positive_ratio: float = Field(..., description="Proportion of positive comments")
    neutral_ratio: float = Field(..., description="Proportion of neutral comments")
    negative_ratio: float = Field(..., description="Proportion of negative comments")
    dominant_sentiment: str = Field(..., description="Most common sentiment")
    common_keywords: List[str] = Field(
        default_factory=list, description="Most frequent keywords in the batch"
    )
    comment_ids: List[str] = Field(
        default_factory=list, description="List of comment IDs included in the analysis"
    )
    processed_texts: List[str] = Field(
        default_factory=list, description="List of texts that were processed"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


from pymongo import MongoClient
from fastapi_app.settings.models import AnalysisSummaryModel


class SummaryStorageProvider:
    """Handles storage of sentiment analysis summaries in MongoDB."""

    def __init__(
        self,
        mongo_uri: str = "mongodb://localhost:27017",
        db_name: str = "ai_dashboard",
    ):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db["analysis_summaries"]

    def save_summary(self, summary: AnalysisSummaryModel) -> str:
        """Insert a summary into the MongoDB collection."""
        result = self.collection.insert_one(summary.dict())
        return str(result.inserted_id)

    def get_summary_by_id(self, summary_id: str) -> dict:
        """Retrieve a summary by its ID."""
        return self.collection.find_one({"summary_id": summary_id})
