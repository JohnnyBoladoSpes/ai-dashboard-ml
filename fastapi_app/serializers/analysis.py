import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field


class AnalysisRequestSerializer(BaseModel):
    """Serializer for AnalysisRequestModel."""

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
    media_id: str = Field(
        description="Media ID of the post (used to avoid re-analysis)"
    )
    business_id: str = Field(description="Business ID associated with the request")

    class Config:
        orm_mode = True


class IndividualCommentResponse(BaseModel):
    """Represents the sentiment analysis result for an individual comment."""

    comment_id: str
    sentiment: str
    confidence: float
    keywords: Optional[List[str]] = []
    topics: Optional[List[str]] = []


class SentimentAnalysisSummaryResponse(BaseModel):
    """Represents a summary of sentiment analysis over multiple comments."""

    total_comments: int
    positive_ratio: float
    neutral_ratio: float
    negative_ratio: float
    common_keywords: List[str]
    dominant_sentiment: str


class SentimentAnalysisResponseSerializer(BaseModel):
    """Represents the sentiment analysis data for a batch of comments."""

    comments: List[IndividualCommentResponse]
    summary: SentimentAnalysisSummaryResponse
