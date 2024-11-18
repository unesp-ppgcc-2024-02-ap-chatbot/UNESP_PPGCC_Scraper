from sentence_transformers import SentenceTransformer
from pathlib import Path
from utils import ROOT_FOLDER, remove_escape_characters
from qdrant_client import models, QdrantClient
from utils import remove_markdown
from dotenv import load_dotenv
import os
import warnings
import json
from fastembed.sparse.bm25 import Bm25
from tqdm import tqdm

load_dotenv()

qdrant_url = os.getenv("QDRANT_URL")
is_local = "localhost" in qdrant_url

if is_local:
    print("Using local Qdrant")
    client = QdrantClient(url=qdrant_url,api_key=os.getenv("QDRANT_API_KEY"))
else:
    client = QdrantClient(
                url=qdrant_url,
                port=None,
                host=None,
                https=True,
                timeout=60,
                api_key=os.getenv("QDRANT_API_KEY")
            )


warnings.filterwarnings("ignore")

def main():
    chunks_file_path = Path(
        ROOT_FOLDER,
        "02-preprocessed-data",
        "01-chunks_data.json"
    )
    chunks = []
    with open(chunks_file_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
        
    for chunk in chunks:
        title = chunk["main_title"]
        chunk["markdown_content"] = chunk["content"]
        chunk["content"] = title + "\n" + remove_markdown(remove_escape_characters(chunk["content"]))
    
    collection_name = os.getenv("QDRANT_COLLECTION_NAME")
    bm25_embedding_model = Bm25("Qdrant/bm25", language="portuguese")
    bge_m3 = SentenceTransformer(
        "BAAI/bge-m3", 
        trust_remote_code=True,
        device="cuda"
    )
        
    client.delete_collection(collection_name)
    print(f"Uploading {len(chunks)} documents to collection {collection_name}")
    
    print(f"Creating collection {collection_name}")
    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "bge-m3": models.VectorParams(
                size=bge_m3.get_sentence_embedding_dimension(), 
                distance=models.Distance.COSINE
            )
        },
        sparse_vectors_config={
            "bm25": models.SparseVectorParams(
                modifier=models.Modifier.IDF,
            )
        }
    )
    
    print("Computing embeddings - bm25...")
    bm25_embeddings = list(bm25_embedding_model.passage_embed([doc["content"] for doc in chunks]))
    print("Uploading points...")
    
    batch_size = 10
    for i in tqdm(range(0, len(chunks), batch_size), desc="Uploading points in batches"):
        batch_chunks = chunks[i:i + batch_size]
        batch_bm25_embeddings = bm25_embeddings[i:i + batch_size]

        client.upload_points(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=idx + i, 
                    vector={
                        "bge-m3": bge_m3.encode(doc["content"]).tolist(),
                        "bm25": batch_bm25_embeddings[idx].as_object()
                    }, 
                    payload=doc
                )
                for idx, doc in enumerate(batch_chunks)
            ],
        )
    print("Done!")


main()
