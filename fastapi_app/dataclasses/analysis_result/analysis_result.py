from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any


@dataclass
class AnalysisResultData:
    """Represents the result of a text analysis."""

    comment_id: str
    sentiment: str
    _id: Optional[str] = None
    confidence: Optional[float] = None
    keywords: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CreateAnalysisResultRequestData:
    comment_id: str
    sentiment: str
    confidence: float
    keywords: Optional[List[str]] = None
    topics: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CreateAnalysisRequestData:
    """Dataclass for handling analysis request data."""

    comment_id: str
    user_id: str
    text: str
    company_id: Optional[str] = None
    source: Optional[str] = None
    requested_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
