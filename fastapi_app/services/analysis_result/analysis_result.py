from fastapi_app.dataclasses.analysis_result.analysis_result import AnalysisResultData
from fastapi_app.dataclasses.models_ia import IndividualCommentAnalysis
from fastapi_app.providers.analysis_result import AnalysisResultProvider


class AnalysisResultService:
    def __init__(self):
        self.provider = AnalysisResultProvider()

    def create(self, request: IndividualCommentAnalysis) -> AnalysisResultData:
        return self.provider.create(request)
