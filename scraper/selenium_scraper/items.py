"""
Web Scraping Data Models

This module defines dataclasses used for storing and organizing data collected
during web scraping operations. These classes represent different types of content
and metadata that can be extracted from web pages.

Classes:
    LinkItem: Represents a link extracted from a web page.
    PageContentItem: Represents the content and metadata of a scraped web page.
    ExternalContentItem: Represents metadata for external content (e.g., downloadable files) found on a web page.

Each class uses default values and optional fields to allow for flexible data collection.
The 'scrape_date' field is automatically set to the current date for all items.

Dependencies:
    - dataclasses
    - datetime
    - typing
    - pathlib
"""


# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from pathlib import Path


@dataclass
class LinkItem:
    """
    Represents a link extracted from a web page.

    Attributes:
        link (Optional[str]): The URL of the extracted link. Defaults to None.
        scrape_date (Optional[str]): The date when the link was scraped, in 'YYYY-MM-DD' format.
                                     Defaults to the current date.
    """
    link: Optional[str] = field(default=None)
    scrape_date: Optional[str] = field(default=date.today().strftime("%Y-%m-%d"))


@dataclass
class PageContentItem:
    """
    Represents the content and metadata of a scraped web page.

    Attributes:
        page_id (Optional[str]): A unique identifier for the page. Defaults to None.
        page_name (Optional[str]): The name or title of the page. Defaults to None.
        page_url (Optional[str]): The URL of the page. Defaults to None.
        page_last_update (Optional[str]): The date of the last update to the page. Defaults to None.
        page_content_html (Optional[str]): The HTML content of the page. Defaults to None.
        page_content_md (Optional[str]): The Markdown content of the page (if available). Defaults to None.
        scrape_date (Optional[str]): The date when the page was scraped, in 'YYYY-MM-DD' format.
                                     Defaults to the current date.
    """
    page_id: Optional[str] = field(default=None)
    page_name: Optional[str] = field(default=None)
    page_url: Optional[str] = field(default=None)
    page_last_update: Optional[str] = field(default=None)
    page_content_html: Optional[str] = field(default=None)
    page_content_md: Optional[str] = field(default=None)
    scrape_date: Optional[str] = field(default=date.today().strftime("%Y-%m-%d"))


@dataclass
class ExternalContentItem:
    """
    Represents metadata for external content (e.g., downloadable files) found on a web page.

    Attributes:
        file_origin (Optional[str]): The URL of the page where the file was found. Defaults to None.
        file_name (Optional[str]): The name of the file. Defaults to None.
        file_format (Optional[str]): The format or extension of the file. Defaults to None.
        file_url (Optional[str]): The URL where the file can be downloaded. Defaults to None.
        file_download_location (Optional[str|Path]): The local path where the file is saved.
                                                     Can be a string or Path object. Defaults to None.
        md_file_path (Optional[str|Path]): The path to a Markdown version of the file, if applicable.
                                           Can be a string or Path object. Defaults to None.
        scrape_date (Optional[str]): The date when the file metadata was scraped, in 'YYYY-MM-DD' format.
                                     Defaults to the current date.
    """
    file_origin: Optional[str] = field(default=None)
    file_name: Optional[str] = field(default=None)
    file_format: Optional[str] = field(default=None)
    file_url: Optional[str] = field(default=None)
    file_download_location: Optional[str|Path] = field(default=None)
    md_file_path: Optional[str|Path] = field(default=None)
    img_file_paths: Optional[list[str]] = field(default=None)
    scrape_date: Optional[str] = field(default=date.today().strftime("%Y-%m-%d"))
