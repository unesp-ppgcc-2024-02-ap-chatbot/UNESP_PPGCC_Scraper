from fastapi import FastAPI
from typing import Literal

from unesp_searcher import UNESPSearcher

app = FastAPI()
collection_name = "unesp"
unesp_searcher = UNESPSearcher(collection_name=collection_name)

@app.get("/api/search")
def search(q: str, 
           result_limit: int = 5, 
           filter_type: Literal["page", "document"] = None):
    return {"result": unesp_searcher.search(text=q, result_limit=result_limit, filter_type=filter_type)}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8055)
