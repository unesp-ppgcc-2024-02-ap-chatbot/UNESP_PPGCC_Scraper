from dotenv import load_dotenv
import os
import pathlib
import re
import rapidjson as json
from pathlib import Path
load_dotenv()

CMD_FOLDER = pathlib.Path(os.getcwd())
ROOT_FOLDER = os.getenv("ROOT_FOLDER") if os.getenv("ROOT_FOLDER") else CMD_FOLDER
page_remove_list = Path(ROOT_FOLDER, "02-preprocessed-data", "utils", "remove-list.json")
page_titles_list = Path(ROOT_FOLDER, "02-preprocessed-data", "utils", "page_titles.json")

def filter_chunks(data):
    with open(page_remove_list, 'r', encoding='utf-8') as f:
        remove_list = json.load(f)
        
    files_to_remove = [chunk['document'] for chunk in remove_list]
    filter1 = [chunk for chunk in data if chunk['file_name'] not in files_to_remove]
    print(f"Removed {len(data) - len(filter1)} chunks.")

    file_name_remove_filter = ["ata", "pauta", "convocacao", "egressos"]
    filter2 = [chunk for chunk in filter1 if not any(x in chunk['file_name'] for x in file_name_remove_filter)]
    removed_list = [chunk for chunk in filter1 if chunk not in filter2]
    for chunk in removed_list:
        print(f"Removed: {chunk['file_name']}")

    print(f"Removed {len(filter1) - len(filter2)} chunks.")
    return filter2


def remove_empty_lines(content: str) -> str:
	# Split the content by lines
	lines = content.splitlines()

	# Remove leading and trailing spaces from each line, adding space for empty lines
	cleaned_lines = []

	for line in lines:
		if line.strip():  # If the line is not empty
			cleaned_lines.append(line.strip())
		else:
			cleaned_lines.append(' ')  # Replace empty line with a space

	# Join the cleaned lines back into a single string
	return ' \n '.join(cleaned_lines)

def remove_markdown(text: str) -> str:
    # we are keeping the links
    text = re.sub(r'(\*\*|__|~~|`|>|#|\*|-)', '', text)
    return text

def add_page_titles(data):
	with open(page_titles_list, 'r', encoding='utf-8') as f:
		page_titles = json.load(f)
	for chunk in data:
		# search for an item with the same file_name
		page_title = next((item for item in page_titles if item["file_name"] == chunk["file_name"]), None)
		if page_title:
			chunk["main_title"] = page_title["main_title"]
		else:
			raise Exception(f"Page title not found for {chunk['file_name']}")
	return data

		