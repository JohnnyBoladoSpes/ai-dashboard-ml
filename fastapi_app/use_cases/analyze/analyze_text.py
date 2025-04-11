from typing import List

from fastapi_app.dataclasses.analysis_result import CreateAnalysisRequestData
from fastapi_app.dataclasses.models_ia import (
    SentimentalAnalysisData,
)
from fastapi_app.models import SentimentAnalyzerBuilder
from fastapi_app.services import AnalysisResultService, SummaryResultService


class AnalyzeTextUseCase:
    def __init__(self):
        self.analysis_service = AnalysisResultService()
        self.summary_service = SummaryResultService()
        self.sentiment_builder_model = SentimentAnalyzerBuilder()

    def execute(
        self, comments: List[CreateAnalysisRequestData]
    ) -> SentimentalAnalysisData:
        media_ids = [c.media_id for c in comments if c.media_id]
        if not media_ids:
            raise ValueError("No media_id found in the request.")

        media_id = media_ids[0]
        if self.analysis_service.is_recently_analyzed(media_id):
            raise ValueError("This media_id has already been analyzed recently.")

        sentimental_analysis = self.sentiment_builder_model.run(comments)
        self.analysis_service.create(sentimental_analysis.comments, media_id)
        self.summary_service.create(sentimental_analysis.summary)
        return sentimental_analysis
