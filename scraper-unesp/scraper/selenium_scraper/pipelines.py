
"""
Selenium Scraper Pipeline Module

This module contains the SeleniumScraperPipeline class, which is responsible for
processing items scraped by Selenium in a Scrapy project. The pipeline handles
different types of scraped items and performs various preprocessing tasks.

Key Components:
- SeleniumScraperPipeline: Main class for processing scraped items.
- process_item: Method to route items to appropriate handlers based on their type.
- handle_page_content_item: Processes PageContentItem objects.
- handle_external_content_item: Processes ExternalContentItem objects.
- replace_links: Utility method to replace relative links with absolute links in HTML.

The pipeline supports the following item types:
- ExternalContentItem: For handling external content like PDF or DOC files.
- PageContentItem: For processing HTML page content.
- LinkItem: For handling scraped links (passed through without modification).

Dependencies:
- re: For regular expressions used in link replacement.
- pathlib: For file path handling.
- markdownify: For converting HTML to Markdown.
- scrapy: For Spider and Item classes, and project settings.
- Custom utility functions for file conversion and saving.

Usage:
This pipeline should be added to the ITEM_PIPELINES setting in your Scrapy project's
settings.py file. It will then automatically process items as they are yielded by your spiders.

Note:
Ensure that all required dependencies are installed and that the necessary utility
functions are available in the project's utils module.
"""

import re
from pathlib import Path
from typing import Union
from markdownify import markdownify as md
from scrapy.spiders import Spider
from scrapy.item import Item
from scrapy.utils.project import get_project_settings
from .items import ExternalContentItem, LinkItem, PageContentItem
from .utils import (
    convert_doc_to_pdf,
    convert_pdf_to_markdown,
    convert_pdf_to_png,
    save_file,
)

SETTINGS = get_project_settings()

class SeleniumScraperPipeline:
    """
    A pipeline for processing items scraped by Selenium in a Scrapy project.

    This pipeline handles different types of items (ExternalContentItem, PageContentItem, LinkItem)
    and performs various preprocessing tasks such as converting file formats, saving content,
    and adjusting metadata.
    """
    def process_item(self, item: Item, spider: Spider) -> Item:
        """
        Process an item based on its type.

        Args:
            item (Item): The scraped item to process.
            spider (Spider): The spider that scraped the item.

        Returns:
            Item: The processed item.
        """
        item_handlers = {
            ExternalContentItem: self.handle_external_content_item,
            PageContentItem: self.handle_page_content_item,
            LinkItem: lambda x, _: x  # Pass-through for LinkItem
        }
        handler = item_handlers.get(type(item))
        return handler(item, spider) if handler else item

    def handle_page_content_item(
        self, item: PageContentItem, spider: Spider
    ) -> PageContentItem:
        """
        Handle processing of PageContentItem.

        This method adjusts page ID, saves HTML content, converts HTML to Markdown,
        and updates the item with file paths.

        Args:
            item (PageContentItem): The page content item to process.
            spider (Spider): The spider that scraped the item.

        Returns:
            PageContentItem: The processed page content item.
        """
        item.page_id = self._clean_page_id(item.page_id)
        file_name = self._generate_file_name(item.page_url)

        html_file_path = self._save_html_content(file_name, item.page_content_html)
        md_file_path = self._save_markdown_content(file_name, item.page_content_html)

        item.page_content_html = html_file_path
        item.page_content_md = md_file_path
        return item

    def handle_external_content_item(
        self, item: ExternalContentItem, spider: Spider
    ) -> ExternalContentItem:
        """
        Handle processing of ExternalContentItem.

        This method converts document files to PDF if necessary, converts PDF to Markdown,
        converts PDF to images, and updates the item with file paths.

        Args:
            item (ExternalContentItem): The external content item to process.
            spider (Spider): The spider that scraped the item.

        Returns:
            ExternalContentItem: The processed external content item.

        Raises:
            ValueError: If the file format is not supported.
        """
        pdf_file_location = self._ensure_pdf_format(item)
        item.md_file_path = self._convert_pdf_to_markdown(pdf_file_location)
        item.img_file_paths = self._convert_pdf_to_images(pdf_file_location)
        item.file_download_location = str(Path(item.file_download_location).resolve())
        return item

    @staticmethod
    def _clean_page_id(page_id: Union[str, None]) -> Union[str, None]:
        """
        Clean the page ID by extracting the last part after a colon and stripping whitespace.

        Args:
            page_id (Union[str, None]): The original page ID.

        Returns:
            Union[str, None]: The cleaned page ID or None if the input was None.
        """
        return page_id.split(":")[-1].strip() if page_id else None

    @staticmethod
    def _generate_file_name(page_url: str) -> str:
        """
        Generate a file name from a page URL.

        Args:
            page_url (str): The URL of the page.

        Returns:
            str: A file name generated from the last two parts of the URL.
        """
        parts = page_url.rstrip('/').split('/')
        return "_".join(parts[-2:])

    def _save_html_content(self, file_name: str, content: str) -> Path:
        """
        Save HTML content to a file.

        Args:
            file_name (str): The name of the file to save.
            content (str): The HTML content to save.

        Returns:
            Path: The path to the saved file.
        """
        html_file_path = SETTINGS.get("RAW_DATA_FOLDERS_BASE_PATHS").get("PAGE_CONTENT").joinpath("html")
        return self._save_file(f"{file_name}.html", html_file_path, content)

    def _save_markdown_content(self, file_name: str, html_content: str) -> Path:
        """
        Convert HTML content to Markdown and save it to a file.

        Args:
            file_name (str): The name of the file to save.
            html_content (str): The HTML content to convert and save.

        Returns:
            Path: The path to the saved Markdown file.
        """
        md_content = self._html_to_markdown(html_content)
        md_file_path = SETTINGS.get("PREPROCESSED_DATA_FOLDERS_BASE_PATHS").get("PAGE_CONTENT").joinpath("markdown")
        return self._save_file(f"{file_name}.md", md_file_path, md_content)

    def _html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML content to Markdown, removing all  <img> tags and all "javascript:void(0);" function calls.

        Args:
            html_content (str): The HTML content to convert.

        Returns:
            str: The converted Markdown content.
        """
        html_content = self.replace_links(html_content)
        md_content = md(html_content, strip=["img"])
        return md_content.replace("(javascript:void(0);)", "")

    @staticmethod
    def _save_file(file_name: str, output_directory: str|Path, content: str) -> Path:
        """
        Save content to a file.

        Args:
            file_name (str): The name of the file to save.
            output_directory (Path): The directory to save the file in.
            content (str): The content to save.

        Returns:
            Path: The path to the saved file.
        """
        file = save_file(file_name=file_name, output_directory=output_directory, content=content)
        return file.resolve()

    def _ensure_pdf_format(self, item: ExternalContentItem) -> Path:
        """
        Ensure that the file is in PDF format, converting if necessary.

        Args:
            item (ExternalContentItem): The item containing the file to process.

        Returns:
            Path: The path to the PDF file.

        Raises:
            ValueError: If the file format is not supported.
        """
        if item.file_format in ["doc", "docx"]:
            return convert_doc_to_pdf(
                doc_file_path=item.file_download_location,
                output_directory=Path(item.file_download_location).parent,
            )
        elif item.file_format != "pdf":
            raise ValueError(f"Unsupported file format: .{item.file_format}. Only .doc, .docx, and .pdf are supported.")
        return Path(item.file_download_location)

    def _convert_pdf_to_markdown(self, pdf_file_path: Path) -> Path:
        """
        Convert a PDF file to Markdown.

        Args:
            pdf_file_path (Path): The path to the PDF file to convert.

        Returns:
            Path: The path to the converted Markdown file.
        """
        md_base_dir = SETTINGS.get("PREPROCESSED_DATA_FOLDERS_BASE_PATHS").get("EXTERNAL_CONTENT").joinpath("markdown")
        return convert_pdf_to_markdown(pdf_file_path=pdf_file_path, output_directory=md_base_dir).resolve()

    def _convert_pdf_to_images(self, pdf_file_path: Path) -> list[Path]:
        """
        Convert a PDF file to a series of images.

        Args:
            pdf_file_path (Path): The path to the PDF file to convert.

        Returns:
            list[Path]: A list of paths to the converted image files.
        """
        img_base_dir = SETTINGS.get("PREPROCESSED_DATA_FOLDERS_BASE_PATHS").get("EXTERNAL_CONTENT").joinpath("png")
        return convert_pdf_to_png(pdf_file_path=pdf_file_path, output_directory=img_base_dir)

    @staticmethod
    def replace_links(html_string: str) -> str:
        """
        Replace relative links in HTML with absolute links.

        Args:
            html_string (str): The HTML string containing links to be replaced.

        Returns:
            str: The HTML string with replaced links.
        """
        base_url = "https://www.ibilce.unesp.br/"
        patterns = [
            (r'href="(Home/[^"]*)"', f'href="{base_url}\\1"'),
            (r'href="(#!/[^"]*)"', f'href="{base_url}\\1"'),
        ]
        for pattern, replacement in patterns:
            html_string = re.sub(pattern, replacement, html_string)
        return html_string
