from typing import Dict, List

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

    def analyze_batch(
        self, comments: List[CreateAnalysisRequestData]
    ) -> SentimentalAnalysisData:
        """Analyze a batch of comments and return an aggregated result."""
        comment_results: List[IndividualCommentAnalysis] = []
        sentiments = []
        words = []

        for comment in comments:
            analysis = self.analyze(comment.text)
            sentiments.append(analysis["sentiment"])
            comment_results.append(
                IndividualCommentAnalysis(
                    comment_id=comment.comment_id,
                    sentiment=analysis["sentiment"],
                    confidence=analysis["confidence"],
                )
            )
            words.extend(comment.text.split())

        # Calculate sentiment proportions
        positive_count = sentiments.count(POSITIVE)
        neutral_count = sentiments.count(NEUTRAL)
        negative_count = sentiments.count(NEGATIVE)

        total_comments = len(comments)
        if total_comments > 0:
            positive_ratio = positive_count / total_comments
            neutral_ratio = neutral_count / total_comments
            negative_ratio = negative_count / total_comments
        else:
            positive_ratio = neutral_ratio = negative_ratio = 0

        # Count word frequencies
        word_frequencies = {}
        for word in words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

        # Sort words by frequency
        sorted_words = sorted(
            word_frequencies.items(), key=lambda item: item[1], reverse=True
        )

        # Determine dominant sentiment
        dominant_sentiment = (
            POSITIVE
            if positive_ratio >= max(neutral_ratio, negative_ratio)
            else (
                NEUTRAL
                if neutral_ratio >= max(positive_ratio, negative_ratio)
                else NEGATIVE
            )
        )

        sentimental_summary = SentimentAnalysisSummary(
            positive_ratio=positive_ratio,
            neutral_ratio=neutral_ratio,
            negative_ratio=negative_ratio,
            common_keywords=[word for word, _ in sorted_words[:10]],
            dominant_sentiment=dominant_sentiment,
            total_comments=total_comments,
        )

        return SentimentalAnalysisData(
            comments=comment_results,
            summary=sentimental_summary,
        )
