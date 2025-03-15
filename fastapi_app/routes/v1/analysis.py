from fastapi import APIRouter

from fastapi_app.views.v1.analysis import AnalysisView

router = APIRouter()

router.post("/analyze")(AnalysisView.analyze_text)
