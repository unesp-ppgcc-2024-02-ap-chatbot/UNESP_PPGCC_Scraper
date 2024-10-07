# UNESP_PPGCC_Scraper

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![Static Badge](https://img.shields.io/badge/License-MIT-green)](LICENSE.txt)

UNESP_PPGCC_Scraper is a web scraping tool designed to extract and process information from the IBILCE UNESP website (www.ibilce.unesp.br), with a specific focus on the Computer Science graduate program pages. This project utilizes the power of Scrapy and Selenium to handle dynamic, JavaScript-rendered content, ensuring comprehensive data collection from web pages. It also implements a Scrapy pipeline for post-scraping operations:

- HTML to Markdown conversion
- Relative to absolute link conversion
- External file download and conversion (e.g., PDF to PNG)


## Table of Contents
- [UNESP\_PPGCC\_Scraper](#unesp_ppgcc_scraper)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
    - [Step 1: Scrape Links](#step-1-scrape-links)
    - [Step 2: Extract Page Content](#step-2-extract-page-content)
    - [Step 3: Download External Content](#step-3-download-external-content)
  - [Output](#output)
  - [Project Structure](#project-structure)
  - [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
1. [Python 3.11](https://www.python.org/downloads/release/python-3110/)
2. [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads/version-selection)
3. [LibreOffice](https://pt-br.libreoffice.org/) (accessible via the 'soffice' command)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/unesp-ppgcc-2024-02-ap-chatbot/UNESP_PPGCC_Scraper.git
   cd repo_name/scraper
   ```

2. Create and activate a virtual environment:
   ```bash
   # Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download ChromeDriver and place the `.exe` file in the `./scraper/` folder.

5. Replace the following files in your virtual environment:
   ```
   .venv/lib/python3.11/site-packages/scrapy_selenium/http.py
   .venv/lib/python3.11/site-packages/scrapy_selenium/middlewares.py
   ```
   with the files provided in `./scraper/scrapy-selenium-update/`.

## Usage

All commands should be run from the `./scraper-unesp/scraper` directory.

### Step 1: Scrape Links

```bash
scrapy crawl links_spider -o "./data/metadata/links_metadata.csv" -t csv
```

This step scrapes all links from Unesp's Graduate Program in Computer Science (PPGCC) pages and saves them to a CSV file.

### Step 2: Extract Page Content

```bash
scrapy crawl page_content_spider -o "./data/metadata/page_content_metadata.csv" -t csv
```

This step extracts the main content from each page, saves HTML snippets, and converts them to Markdown format.

### Step 3: Download External Content

```bash
scrapy crawl external_content_spider -o "./data/metadata/external_content_metadata.csv" -t csv
```

This step downloads external files referenced on the pages, converts them to Markdown, and generates PNG images of the content.

## Output

The scraper produces the following output files:

1. `links_metadata.csv`: Contains scraped links and their metadata.
2. `page_content_metadata.csv`: Contains information about extracted page content.
3. `external_content_metadata.csv`: Contains information about downloaded external files.

[Add more details about the structure and location of output files if necessary]

## Project Structure
```project
./
├── LICENSE.txt
├── README.MD
├── requirements.txt
├── scraper
│   ├── chromedriver
│   ├── data
│   │   ├── metadata
│   │   │   ├── external_content_metadata.csv
│   │   │   ├── links_metadata.csv
│   │   │   └── page_content_metadata.csv
│   │   ├── preprocessed
│   │   │   ├── external_content
│   │   │   │   ├── markdown
│   │   │   │   └── png
│   │   │   └── page_content
│   │   │       └── markdown
│   │   └── raw
│   │       ├── external_content
│   │       └── page_content
│   │           └── html
│   ├── scrapy.cfg
│   └── selenium_scraper
│       ├── items.py
│       ├── middlewares.py
│       ├── pipelines.py
│       ├── settings.py
│       ├── spiders
│       │   └── scraping.py
│       └── utils.py
└── scrapy-selenium-update
    ├── http.py
    └── middlewares.py
```

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.