from fastapi import FastAPI
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()

from unesp_searcher import UNESPSearcher

app = FastAPI()
collection_name = os.getenv("QDRANT_COLLECTION_NAME")
unesp_searcher = UNESPSearcher(collection_name=collection_name)

@app.get("/api/search_semantic")
def search_semantic(q: str, 
           result_limit: int = 5):
    return {"result": unesp_searcher.search_semantic(text=q, result_limit=result_limit)}

@app.get("/api/search_hybrid_rerank")
def search_semantic(q: str, 
           result_limit: int = 5):
    return {"result": unesp_searcher.search_hybrid_rerank(text=q, result_limit=result_limit)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8055)
