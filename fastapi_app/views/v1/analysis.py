from typing import Dict

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/analyze")
def analyze_text(data: Dict[str, str]) -> Dict[str, str]:
    """Analyzes the input text and returns a simulated sentiment."""
    if "text" not in data:
        raise HTTPException(status_code=400, detail="Missing 'text' field")

    # Simulated AI analysis
    result = {"text": data["text"], "sentiment": "positive"}
    return result
