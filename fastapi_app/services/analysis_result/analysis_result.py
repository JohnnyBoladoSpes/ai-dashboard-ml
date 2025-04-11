from fastapi_app.dataclasses.analysis_result.analysis_result import AnalysisResultData
from fastapi_app.dataclasses.models_ia import IndividualCommentAnalysis
from fastapi_app.providers.analysis_result import AnalysisResultProvider
from typing import List


class AnalysisResultService:
    def __init__(self):
        self.provider = AnalysisResultProvider()

    def create(
        self, request: List[IndividualCommentAnalysis], media_id: str
    ) -> AnalysisResultData:
        self.provider.mark_as_analyzed(media_id)
        return self.provider.create_many_results(request)

    def is_recently_analyzed(self, media_id: str) -> bool:
        return self.provider.is_recently_analyzed(media_id)
