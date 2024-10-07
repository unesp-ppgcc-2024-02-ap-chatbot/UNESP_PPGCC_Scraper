from sentence_transformers import SentenceTransformer
from pathlib import Path
from utils import ROOT_FOLDER
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)
from qdrant_client import models, QdrantClient
from utils import remove_empty_lines
from dotenv import load_dotenv
import os

load_dotenv()
client = QdrantClient(url=os.getenv("QDRANT_URL"))

def get_markdown_list(markdown_dir: Path, type: str) -> list[dict[str, str]]:
    # List to store the content of each markdown file
    markdown_content_list = []

    # Loop through all markdown files and store their file name and content in a dictionary
    for markdown_file in markdown_dir.rglob("*.md"):
        with markdown_file.open("r", encoding="utf-8") as file:
            content = file.read()
            markdown_content_list.append({
                "file_name": markdown_file.name,  # Get just the file name
                "content": content,
                "type": type
            })
    
    return markdown_content_list


def get_chuncks():
    markdown_dir = Path(
        ROOT_FOLDER, 
        "data", 
        "preprocessed", 
        "page_content", 
        "markdown"
    )
    markdown_page_list = get_markdown_list(markdown_dir, "page")
    
    markdown_external_content_dir = Path(
        ROOT_FOLDER, 
        "data", 
        "preprocessed", 
        "external_content", 
        "markdown"
    )
    markdown_external_content_list = get_markdown_list(
        markdown_external_content_dir,
        "document"    
    )
    # combine the two lists
    markdown_list = markdown_page_list + markdown_external_content_list
    
    chunk_size = 1000
    chunk_overlap = 250

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )

    results = []
    for doc in markdown_list:
        markdown_document = remove_empty_lines(doc["content"])
        file_name = doc["file_name"]
        splits = text_splitter.split_text(markdown_document)
        for split in splits:
            results.append({
                "file_name": file_name,
                "content": split,
                "full_content": markdown_document,
                "type": doc["type"]
            })
            # print(split)
            # print("=====================================")
    return results

def main():
    chuncks = get_chuncks()
    collection_name = "unesp"
    model = SentenceTransformer(
        "jinaai/jina-embeddings-v3", 
        trust_remote_code=True,
        device="cuda"
    )
    client.delete_collection(collection_name)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=model.get_sentence_embedding_dimension(), 
            distance=models.Distance.COSINE,
        ),
    )
    client.upload_points(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=idx, vector=model.encode(doc["content"]).tolist(), payload=doc
            )
            for idx, doc in enumerate(chuncks)
        ],
    )


main()