import random
from fastapi_app.dataclasses.analysis_result import (
    AnalysisResultData,
    CreateAnalysisResultRequestData,
)

from fastapi_app.services import AnalysisResultService


class AnalyzeTextUseCase:
    def __init__(self):
        self.service = AnalysisResultService()

    def _analyze_sentiment(self) -> str:
        return random.choice(["positive", "neutral", "negative"])

    def _get_confidence(self) -> float:
        return round(random.uniform(0.75, 0.99), 2)

    def execute(self, request: CreateAnalysisResultRequestData) -> AnalysisResultData:
        sentiment = self._analyze_sentiment()
        confidence = self._get_confidence()
        keywords = ["example", "keyword"]
        topics = ["example topic"]

        analysis_request = CreateAnalysisResultRequestData(
            request_id=request.request_id,
            sentiment=sentiment,
            confidence=confidence,
            keywords=keywords,
            topics=topics,
        )

        return self.service.create(analysis_request)
