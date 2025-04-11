from typing import List

from fastapi_app.dataclasses.analysis_result import CreateAnalysisRequestData
from fastapi_app.dataclasses.models_ia import (
    SentimentalAnalysisData,
)
from fastapi_app.models import SentimentAnalysisModel, SentimentAnalyzerBuilder
from fastapi_app.services import AnalysisResultService, SummaryResultService


class AnalyzeTextUseCase:
    def __init__(self):
        self.analysis_service = AnalysisResultService()
        self.summary_service = SummaryResultService()
        self.sentiment_builder_model = SentimentAnalyzerBuilder()

    def execute(
        self, comments: List[CreateAnalysisRequestData]
    ) -> SentimentalAnalysisData:
        sentimental_analysis = self.sentiment_builder_model.run(comments)
        self.analysis_service.create(sentimental_analysis)
        self.summary_service.create(sentimental_analysis)
        return sentimental_analysis
