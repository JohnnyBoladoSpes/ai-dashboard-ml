from fastapi_app.dataclasses.models_ia.sentiment_analysis import (
    CreateSentimentSummaryData,
    SentimentAnalysisSummary,
)
from fastapi_app.providers.summary_result import SummaryResultProvider


class SummaryResultService:
    def __init__(self):
        self.provider = SummaryResultProvider()

    def create(self, request: CreateSentimentSummaryData) -> SentimentAnalysisSummary:
        return self.provider.create(request)
