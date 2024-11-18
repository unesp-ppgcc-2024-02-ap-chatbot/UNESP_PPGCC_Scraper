import pandas as pd
import json
from utils import ROOT_FOLDER
from pathlib import Path

SOURCE_METADATA_DIR = Path(
    ROOT_FOLDER,
    "01-scraper", 
    "scraper",
    "data",
    "metadata"
)

TARGET_METADATA_DIR = Path(
    ROOT_FOLDER,
    "02-preprocessed-data"
)

def csv_to_json_with_id(csv_path, type = 'external'):
    # Load CSV file
    df = pd.read_csv(csv_path)
    prefix = 'ext' if type == 'external' else 'page'
    # Generate custom IDs
    df['id'] = [f"{prefix}_{str(i+1).zfill(3)}" for i in range(len(df))]

    # Convert DataFrame to JSON
    json_data = df.to_dict(orient='records')

    results = []
    md_folder = 'external_content' if type == 'external' else 'page_content'
    # handle some keys
    for item in json_data:
        # get file name from markdown file path string
        result_item = {}
        result_item['id'] = item['id']

        if type == 'external':
            # pdfs
            result_item['markdown_file_name'] = md_folder + "/" + item['md_file_path'].split('/')[-1]
            result_item['origin'] = item['file_origin']
            result_item['name'] = item['file_name']
            result_item['type'] = item['file_format']
            result_item['scrape_date'] = item['scrape_date']
            result_item['url'] = item['file_url']
        else:
            # pages
            result_item['markdown_file_name'] = md_folder + "/" + item['page_content_md'].split('/')[-1]
            result_item['name'] = item['page_name']
            result_item['scrape_date'] = item['scrape_date']
            result_item['url'] = item['page_url']
            result_item['type'] = 'page'
            result_item['last_update'] = item['page_last_update']
            result_item['page_id'] = item['page_id']
            
            
        results.append(result_item)
    return results
        
        


def create_metadata():
    csv_path_external = Path(SOURCE_METADATA_DIR, 'external_content_metadata.csv')
    csv_path_page = Path(SOURCE_METADATA_DIR, 'page_content_metadata.csv')
    json_path = Path(TARGET_METADATA_DIR, 'content_metadata.json')

    data_extenal = csv_to_json_with_id(csv_path_external, "external")
    data_page = csv_to_json_with_id(csv_path_page, "page")
    all_data = data_extenal + data_page
    
    # Save JSON output
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, indent=4, ensure_ascii=False)

    print(f"JSON file created at {json_path}")


if __name__ == "__main__":
    create_metadata()