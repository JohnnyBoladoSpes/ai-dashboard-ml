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
