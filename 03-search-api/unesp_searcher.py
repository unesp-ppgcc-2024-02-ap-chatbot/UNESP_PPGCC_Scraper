from qdrant_client import models
from sentence_transformers import SentenceTransformer
from utils import get_qdrant_client
from typing import Literal

class UNESPSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.model = SentenceTransformer(
            "jinaai/jina-embeddings-v3", 
            trust_remote_code=True,
            device="cpu"
        )
        self.qdrant_client = get_qdrant_client()

    def search(self, 
               text: str, 
               result_limit: int = 5,
               filter_type: Literal["page", "document"] = None):
        # Convert text query into vector
        vector = self.model.encode(text).tolist()
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="type",
                        match=models.MatchValue(
                            value=filter_type,
                        ),
                    )
                ]
            ) if filter_type else None,
            limit=result_limit,  
        ).points
        payloads = [hit.payload for hit in search_result]
        return payloads
