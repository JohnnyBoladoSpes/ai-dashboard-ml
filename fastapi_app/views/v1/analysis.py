from typing import List

from fastapi import APIRouter, HTTPException

from fastapi_app.dataclasses.models_ia import SentimentalAnalysisData
from fastapi_app.serializers import (
    AnalysisRequestSerializer,
)
from fastapi_app.use_cases import AnalyzeTextUseCase

router = APIRouter()


class AnalysisView:
    """API View for handling text analysis requests."""

    @router.post("/analyze", response_model=SentimentalAnalysisData)
    def analyze_text(request: List[AnalysisRequestSerializer]):
        try:
            use_case = AnalyzeTextUseCase()
            result = use_case.execute(request)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
