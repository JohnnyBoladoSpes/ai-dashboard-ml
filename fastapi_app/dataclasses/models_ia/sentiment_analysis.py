from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class IndividualCommentAnalysis:
    """Represents the sentiment analysis result for an individual comment."""

    comment_id: str
    sentiment: str
    confidence: Optional[float] = None
    keywords: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SentimentAnalysisSummary:
    """Represents a summary of sentiment analysis over multiple comments."""

    total_comments: int
    positive_ratio: float
    neutral_ratio: float
    negative_ratio: float
    common_keywords: List[str]
    dominant_sentiment: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SentimentalAnalysisData:
    """Represents the sentiment analysis data for a batch of comments."""

    comments: List[IndividualCommentAnalysis]
    summary: SentimentAnalysisSummary

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CreateSentimentSummaryData:
    comment_ids: List[str]
    positive_ratio: float
    neutral_ratio: float
    negative_ratio: float
    common_keywords: List[str]
    dominant_sentiment: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
