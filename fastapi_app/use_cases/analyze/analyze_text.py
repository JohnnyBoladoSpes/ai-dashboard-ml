from typing import List

from fastapi_app.dataclasses.analysis_result import CreateAnalysisRequestData
from fastapi_app.dataclasses.models_ia import (
    SentimentalAnalysisData,
)
from fastapi_app.models import SentimentAnalysisModel, SentimentAnalyzerBuilder
from fastapi_app.services import AnalysisResultService


class AnalyzeTextUseCase:
    def __init__(self):
        self.service = AnalysisResultService()
        self.sentiment_builder_model = SentimentAnalyzerBuilder()

    def execute(
        self, comments: List[CreateAnalysisRequestData]
    ) -> SentimentalAnalysisData:
        return self.sentiment_builder_model.run(comments)
