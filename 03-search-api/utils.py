from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
load_dotenv()

def get_qdrant_client():
    return QdrantClient(url=os.getenv("QDRANT_URL"))