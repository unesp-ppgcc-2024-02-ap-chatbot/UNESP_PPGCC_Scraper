from pathlib import Path
from utils import ROOT_FOLDER, add_page_titles, filter_chunks
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)
from utils import remove_empty_lines
import json

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def get_markdown_list(markdown_dir: Path, type: str) -> list[dict[str, str]]:
    # List to store the content of each markdown file
    markdown_content_list = []

    # check if the directory and if has files
    if not markdown_dir.exists() or not any(markdown_dir.iterdir()):
        print(f"No markdown files found in {markdown_dir}")

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


def get_chunks():
    markdown_dir = Path(
        ROOT_FOLDER,
        "01-scraper", 
        "scraper",
        "data",
        "preprocessed",
        "page_content", 
        "markdown"
    )
    markdown_page_list = get_markdown_list(markdown_dir, "page")
    
    markdown_external_content_dir = Path(
        ROOT_FOLDER, 
        "01-scraper", 
        "scraper",
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
    
    # get metadata
    metadata_file_path = Path(
        ROOT_FOLDER,
        "02-preprocessed-data",
        "content_metadata.json"
    )
    # Open the file and load the JSON data
    with open(metadata_file_path, 'r', encoding='utf-8') as file:
        metadata = json.load(file)
    
    for doc in markdown_list:
        file_prefix = "page_content" if doc["type"] == "page" else "external_content"
        file_name = file_prefix + "/" + doc["file_name"]
        # search for the metadata
        for item in metadata:
            if item["markdown_file_name"] == file_name:
                doc["metadata"] = item
                break

    all_have_metadata = all('metadata' in doc for doc in markdown_list)

    if all_have_metadata:
        print("All items have a 'metadata' field.")
    else:
        print("Some items are missing the 'metadata' field.")
        raise Exception("Some items are missing the 'metadata' field.")
    
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )

    results = []
    for idx, doc in enumerate(markdown_list):
        markdown_document = remove_empty_lines(doc["content"])
        file_name = doc["file_name"]
        splits = text_splitter.split_text(markdown_document)
        for idx_split, split in enumerate(splits):
            chunk_id = f"{idx + 1}.{idx_split + 1}"
            results.append({
                "chunk_id": chunk_id,
                "file_name": file_name,
                "content": split,
                "full_content": markdown_document,
                "type": doc["type"],
                "metadata": doc["metadata"]
            })
            # print(split)
            # print("=====================================")
    return results

def main():
    chunks = get_chunks()
    number_of_chunks = len(chunks)
    print(f"Total number of chunks: {len(chunks)}")
    chunks = filter_chunks(chunks)
    number_of_chunks_after_filtering = len(chunks)
    print(f"Total number of chunks after filtering: {len(chunks)}")
    chunks = add_page_titles(chunks)
    
    # save chunks to disk
    chunks_file_path = Path(
        ROOT_FOLDER,
        "02-preprocessed-data",
        "01-chunks_data.json"
    )
    # Create the directory if it doesn't exist
    chunks_file_path.parent.mkdir(parents=True, exist_ok=True)
    # Save the data to disk
    with open(chunks_file_path, 'w', encoding='utf-8') as file:
        json.dump(chunks, file, indent=4, ensure_ascii=False)
        
    # save stats
    statis_chunk_file_path = Path(
        ROOT_FOLDER,
        "02-preprocessed-data",
        "chunks_stats.json"
    )
    stats = {
        "total_chunks": number_of_chunks,
        "total_chunks_after_filtering": number_of_chunks_after_filtering,
        "removed_chunks": number_of_chunks - number_of_chunks_after_filtering,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP
    }
    with open(statis_chunk_file_path, 'w', encoding='utf-8') as file:
        json.dump(stats, file, indent=4, ensure_ascii=False)

main()
