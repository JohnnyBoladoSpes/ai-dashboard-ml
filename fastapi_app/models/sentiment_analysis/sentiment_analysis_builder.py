from typing import List

from fastapi_app.dataclasses.analysis_result import CreateAnalysisRequestData
from fastapi_app.dataclasses.models_ia import (
    SentimentalAnalysisData,
)
from fastapi_app.models.text_preprocessor import TextPreprocessor

from .sentiment_analysis import SentimentAnalysisModel


class SentimentAnalyzerBuilder:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.analyzer_model = SentimentAnalysisModel()

    def run(self, comments: List[CreateAnalysisRequestData]) -> SentimentalAnalysisData:
        cleaned_comments = [
            CreateAnalysisRequestData(
                comment_id=comment.comment_id,
                user_id=comment.user_id,
                text=self.preprocessor.clean_text(comment.text),
                business_id=comment.business_id,
                media_id=comment.media_id,
                source=comment.source,
                requested_at=comment.requested_at,
            )
            for comment in comments
        ]

        return self.analyzer_model.analyze_batch(cleaned_comments)
