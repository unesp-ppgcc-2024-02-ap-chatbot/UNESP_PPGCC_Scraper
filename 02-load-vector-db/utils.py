from dotenv import load_dotenv
import os
import pathlib

load_dotenv()

CMD_FOLDER = pathlib.Path(os.getcwd())
ROOT_FOLDER = os.getenv("ROOT_FOLDER") if os.getenv("ROOT_FOLDER") else CMD_FOLDER

def remove_empty_lines(content: str) -> str:
    # Split the content by lines
    lines = content.splitlines()

    # Remove leading and trailing spaces from each line and filter out consecutive empty lines
    cleaned_lines = []

    for line in lines:
        if line.strip():  # If the line is not empty
            cleaned_lines.append(line)

    # Join the cleaned lines back into a single string
    return '\n'.join(cleaned_lines)
