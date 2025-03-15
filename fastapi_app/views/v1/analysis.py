from fastapi_app.dataclasses.analysis_result import (
    AnalysisResultData,
)

from fastapi import APIRouter, HTTPException
from fastapi_app.use_cases import AnalyzeTextUseCase
from fastapi_app.serializers import AnalysisRequestSerializer

router = APIRouter()


class AnalysisView:
    """API View for handling text analysis requests."""

    @staticmethod
    @router.post("/analyze", response_model=AnalysisResultData)
    def analyze_text(request: AnalysisRequestSerializer):
        """Receives a text, processes it using the use case, and returns the result."""
        try:
            use_case = AnalyzeTextUseCase()
            result = use_case.execute(request)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
