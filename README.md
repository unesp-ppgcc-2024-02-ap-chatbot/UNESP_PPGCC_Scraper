# UNESP AI Chatbot

## Getting Started

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

### Scraping

See the [scraping](01-scraper/README.MD) directory.


### Chunking and add chunks to the vector database

Using Qdrant locally:

```bash
docker-compose up -d
```

