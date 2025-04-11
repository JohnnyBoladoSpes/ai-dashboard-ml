import redis
import hashlib
import json
from typing import List
from datetime import timedelta

from fastapi_app.dataclasses.analysis_result import CreateAnalysisRequestData


class RedisSentimentCache:
    def __init__(self, host="localhost", port=6381, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def _generate_key(self, comment: CreateAnalysisRequestData) -> str:
        data = f"{comment.comment_id}:{comment.user_id}:{comment.company_id}:{comment.text}"
        return hashlib.sha256(data.encode()).hexdigest()

    def check_cached_analysis(
        self, comments: List[CreateAnalysisRequestData]
    ) -> List[CreateAnalysisRequestData]:
        """Return only comments not found in cache."""
        uncached_comments = []
        for comment in comments:
            key = self._generate_key(comment)
            if not self.client.exists(key):
                uncached_comments.append(comment)
        return uncached_comments

    def store_analysis(
        self, comments: List[CreateAnalysisRequestData], ttl_hours: int = 2
    ):
        """Store comments in cache to avoid reprocessing."""
        for comment in comments:
            key = self._generate_key(comment)
            self.client.setex(key, timedelta(hours=ttl_hours), value="1")
