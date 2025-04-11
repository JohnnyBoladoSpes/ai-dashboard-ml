from typing import Dict, List

import pandas as pd
from transformers import pipeline

from fastapi_app.dataclasses.analysis_result import CreateAnalysisRequestData
from fastapi_app.dataclasses.models_ia import (
    IndividualCommentAnalysis,
    SentimentalAnalysisData,
    SentimentAnalysisSummary,
)

from .constants import NEGATIVE, NEUTRAL, POSITIVE, SENTIMENT_ANALYSIS


class SentimentAnalysisModel:
    """Handles sentiment analysis using a pre-trained Hugging Face model."""

    def __init__(self):
        """Initialize the pipeline model."""
        self.classifier = pipeline(SENTIMENT_ANALYSIS)

    def analyze(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of the given text and return results."""
        result = self.classifier(text)[0]
        return {"sentiment": result["label"], "confidence": result["score"]}

    @staticmethod
    def get_dominant_sentiment(pos: float, neu: float, neg: float) -> str:
        if pos >= max(neu, neg):
            return POSITIVE
        elif neu >= max(pos, neg):
            return NEUTRAL
        return NEGATIVE

    def analyze_batch(
        self, comments: List[CreateAnalysisRequestData]
    ) -> SentimentalAnalysisData:
        # Analyze each comment in the batch
        comment_results = [
            IndividualCommentAnalysis(
                comment_id=comment.comment_id, **self.analyze(comment.text)
            )
            for comment in comments
        ]

        # Convert results to DataFrame
        df = pd.DataFrame([c.__dict__ for c in comment_results])

        # Sentiment ratios
        total = len(df)
        sentiment_counts = df["sentiment"].value_counts(normalize=True).to_dict()

        positive_ratio = sentiment_counts.get(POSITIVE, 0.0)
        neutral_ratio = sentiment_counts.get(NEUTRAL, 0.0)
        negative_ratio = sentiment_counts.get(NEGATIVE, 0.0)

        # Word frequency
        all_words = " ".join([comment.text for comment in comments]).split()
        word_freq = pd.Series(all_words).value_counts()
        top_keywords = word_freq.head(10).index.tolist()

        # Dominant sentiment
        dominant_sentiment = SentimentAnalysisModel.get_dominant_sentiment(
            positive_ratio, neutral_ratio, negative_ratio
        )

        # Create summary
        summary = SentimentAnalysisSummary(
            positive_ratio=positive_ratio,
            neutral_ratio=neutral_ratio,
            negative_ratio=negative_ratio,
            common_keywords=top_keywords,
            dominant_sentiment=dominant_sentiment,
            total_comments=total,
        )

        return SentimentalAnalysisData(
            comments=comment_results,
            summary=summary,
        )
