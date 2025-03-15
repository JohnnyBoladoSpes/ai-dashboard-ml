from fastapi import APIRouter
from fastapi_app.views.v1.analysis import AnalysisView
from fastapi_app.dataclasses.analysis_result import AnalysisResultData

router = APIRouter()

router.post("/analyze", response_model=AnalysisResultData)(AnalysisView.analyze_text)
