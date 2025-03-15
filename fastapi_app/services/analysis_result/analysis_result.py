from fastapi_app.dataclasses.analysis_result.analysis_result import (
    AnalysisResultData,
    CreateAnalysisResultRequestData,
)
from fastapi_app.providers.analysis_result import AnalysisResultProvider


class AnalysisResultService:
    def __init__(self):
        self.provider = AnalysisResultProvider()

    def create(self, request: CreateAnalysisResultRequestData) -> AnalysisResultData:
        return self.provider.create(request)
