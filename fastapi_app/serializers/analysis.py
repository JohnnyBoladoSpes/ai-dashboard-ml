import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class AnalysisRequestSerializer(BaseModel):
    """Serializer for AnalysisRequestModel."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = Field(..., description="Identifier of the user making the request")
    company_id: Optional[str] = Field(
        None, description="Company related to the request"
    )
    source: Optional[str] = Field(
        None, description="Data source (e.g., Instagram, Twitter, API)"
    )
    text: str = Field(...)
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        orm_mode = True
