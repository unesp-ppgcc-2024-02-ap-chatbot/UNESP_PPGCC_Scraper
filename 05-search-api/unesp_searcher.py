from qdrant_client import models
from sentence_transformers import SentenceTransformer
from fastembed.sparse.bm25 import Bm25
from utils import get_qdrant_client

class UNESPSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.model_bge_m3 = SentenceTransformer(
            "BAAI/bge-m3",
            trust_remote_code=True,
            device="cpu"
        )
        self.model_bm25 =  Bm25("Qdrant/bm25", language="portuguese")        
        self.qdrant_client = get_qdrant_client()


    def search_semantic(self, 
               text: str, 
               result_limit: int = 5):
        
        # Convert text query into vector
        vector = self.model_bge_m3.encode(text).tolist()
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            using="bge-m3",
            query=vector,
            limit=result_limit,  
        ).points
        payloads = [hit.payload for hit in search_result]
        return payloads
    
    
    def search_hybrid_rerank(self, text: str, result_limit: int = 5):
        vector_semantic = self.model_bge_m3.encode(text).tolist()
        bm25_vector = next(self.model_bm25.query_embed(text))
        prefetch_limit = 20
        
        prefetch_list = [
            models.Prefetch(
                query=vector_semantic,
                using="bge-m3",
                limit=prefetch_limit
            ),
            models.Prefetch(
                query=models.SparseVector(**bm25_vector.as_object()),
                using="bm25",
                limit=prefetch_limit
            )
        ]
        
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            prefetch=prefetch_list,
            query=models.FusionQuery(
                fusion=models.Fusion.RRF,
            ),
            limit=result_limit
        )
        return search_result

