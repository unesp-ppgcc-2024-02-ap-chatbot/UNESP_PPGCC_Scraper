# UNESP AI Chatbot

## About

This project is a chatbot that uses a search engine to find answers to questions. The data is scraped from the [UNESP](https://www.ibilce.unesp.br/#!/pos-graduacao/programas-de-pos-graduacao/ciencia-da-computacao/apresentacao/) postgraduate in computer science website.

This is a project for the deep learning course, carried out in the second semester of 2024 by the students:

- André da Fonseca Schuck
- Gabriel Lima
- Wagner Costa Santos

## Getting Started

The search engine is based on the [Qdrant](https://qdrant.com/) vector database.
For details on how to scrape the data, see the [scraping](01-scraper/README.MD) directory.

### Prerequisites

- Python 3.11 or later

### Installation

Install venv:

```bash
python3.11 -m venv .venv
```

Activate venv:

```bash
# Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Note: If you want to run the scraper, you need to install the dependencies in the `01-scraper\requirements.txt` file.

### Scraping

See the [scraping](01-scraper/README.MD) directory.

### Global environment variables

Create a `.env` file in the root directory with the following variables:

```bash
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=someapikey
ROOT_PROJECT_FOLDER=/home/someuser/unesp-chatbot # The root folder of the project
QDRANT_COLLECTION_NAME=UNESP_CHATBOT_PPGCC
```

### Preprocessing

```bash
python 03-preprocess-create-chunks/01-create-metadata.py
```

This script will create a metadata file:

```bash
02-preprocessed-data/content_metadata.json
```

### Chunking content

- To create the chunks we are also using 2 external files from other projects:

```bash
02-preprocessed-data/utils/page_titles.json
02-preprocessed-data/utils/remove-list.json
```

We are using the page_titles.json file to get the titles of the pages (LLM generated). The remove-list.json file is used to ignore some pages that are not relevant to the chatbot (empty pages or pages with only links). We are also removing other pages with old information.

- Preprocess the data and create the chunks:

```bash
python 03-preprocess-create-chunks/02-create-chunks.py
```

Result:

```bash
02-preprocessed-data/01-chunks_data.json
02-preprocessed-data/chunks_stats.json # Stats about the chunks
``` 

### Upload to vector database (Qdrant)

- Using Qdrant locally:

```bash
docker-compose up -d
```

- Upload the data to Qdrant:

```bash
python 04-load-vector-db/main.py
```

We are using `"BAAI/bge-m3"` model to generate the embeddings and we also using BM25 (`"Qdrant/bm25"`) to generate the scores.

### API

The API is a FastAPI application that uses the Qdrant database to search for answers (`05-search-api`).

To run the API:

```bash
python 05-search-api/service.py
```

You can access the API at `http://localhost:8055/docs`.

### Push docker images

```bash
cd 04-chat-app
docker build -t wagnerdev/chatapp-unesp:latest .
docker push wagnerdev/chatapp-unesp:latest
````

```bash
cd 03-search-api
docker build -t wagnerdev/chatapi-unesp:latest .
docker push wagnerdev/chatapi-unesp:latest
```


