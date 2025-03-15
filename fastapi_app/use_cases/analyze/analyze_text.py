from typing import List

from fastapi_app.dataclasses.analysis_result import (
    CreateAnalysisRequestData,
)
from fastapi_app.dataclasses.models_ia import (
    IndividualCommentAnalysis,
    SentimentalAnalysisData,
)
from fastapi_app.models import SentimentAnalysisModel
from fastapi_app.services import AnalysisResultService


class AnalyzeTextUseCase:
    def __init__(self):
        self.service = AnalysisResultService()
        self.sentiment_model = SentimentAnalysisModel()

    def execute(
        self, comments: List[CreateAnalysisRequestData]
    ) -> SentimentalAnalysisData:
        analysis_result = self.sentiment_model.analyze_batch(comments)

        for comment in analysis_result.comments:
            individual_analysis = IndividualCommentAnalysis(
                comment_id=comment.comment_id,
                sentiment=comment.sentiment,
                confidence=comment.confidence,
            )
            self.service.create(individual_analysis)

        return analysis_result
