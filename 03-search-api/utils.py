from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
load_dotenv()

def get_qdrant_client():
    print(os.getenv("QDRANT_URL"))
    print(os.getenv("QDRANT_API_KEY"))
    return QdrantClient(url=os.getenv("QDRANT_URL"),api_key=os.getenv("QDRANT_API_KEY"))