"""
Web Scraping Spiders for IBILCE UNESP

This module contains a collection of Scrapy spiders designed to crawl and extract
information from the IBILCE UNESP website (www.ibilce.unesp.br), specifically
targeting the Computer Science graduate program pages.

The module includes the following spiders:

1. BaseSpider: A base class that provides common functionality for other spiders.
2. LinksSpider: Crawls and extracts links from the specified domain.
3. PageContentSpider: Extracts content from specific pages.
4. ExternalContentSpider: Downloads external content (e.g., PDFs) linked from specific pages.

These spiders use Selenium for JavaScript-rendered content and can handle
dynamic web pages. They are designed to work together to gather information about the 
graduate program.

Usage:
    To use these spiders, you need to have Scrapy and Selenium set up in your
    environment. The spiders can be run using Scrapy's command-line interface
    or can be imported and used in other Scrapy projects.

Dependencies:
    - scrapy
    - scrapy-selenium
    - selenium
    - urllib
    - pathlib
    - csv

Note:
    Make sure to respect the website's robots.txt file and terms of service
    when using these spiders. Adjust the crawling speed and frequency to avoid
    overwhelming the server.
"""

from csv import reader
from collections.abc import Generator
from pathlib import Path
from urllib.parse import urljoin
import time
from typing import Union
from scrapy.http import Response
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ..items import ExternalContentItem, LinkItem, PageContentItem


SETTINGS = get_project_settings()


class BaseSpider(Spider):
    """
    A base spider class that provides common functionality for other spiders.

    This class extends Scrapy's Spider class and provides a method for reading
    links from a CSV file, which is a common operation for multiple spiders
    in this project.

    Attributes:
        Inherits all attributes from scrapy.spiders.Spider.
    """

    @staticmethod
    def _read_links_file(links_metadata_file_path: str | Path) -> list[str] | None:
        """
        Read links from a CSV file.

        Args:
            links_metadata_file_path (str | Path): The path to the CSV file containing links.

        Returns:
            list[str] | None: A list of links read from the file, or None if the file couldn't be read.
        """
        with open(links_metadata_file_path, "r", encoding="utf-8") as links_file:
            return list(reader(links_file))


class LinksSpider(Spider):
    """
    A spider for crawling and extracting links from a specific domain.

    This spider starts from a given URL and follows links within the same domain,
    collecting all unique URLs it encounters.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): The list of allowed domains for crawling.
        start_url (list): The starting URL for the spider.
        links (set): A set to store unique links encountered during crawling.
    """

    name = "links_spider"
    allowed_domains = ["www.ibilce.unesp.br"]
    start_url = [
        "https://www.ibilce.unesp.br/#!/pos-graduacao/programas-de-pos-graduacao/ciencia-da-computacao/"
    ]

    def __init__(self):
        """Initialize the LinksSpider with an empty set of links."""
        self.links = set()

    def start_requests(self) -> Generator[SeleniumRequest]:
        """
        Generate the initial request for the spider.

        Returns:
            Generator[SeleniumRequest]: A generator yielding the initial SeleniumRequest.
        """
        url = "https://www.ibilce.unesp.br/#!/pos-graduacao/programas-de-pos-graduacao/ciencia-da-computacao/"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            wait_time=15,
            wait_until=EC.visibility_of_element_located(
                (By.CLASS_NAME, "wrapper-conteudo-tinymce")
            ),
        )

    def parse(
        self, response: Response
    ) -> Generator[Union[LinkItem, SeleniumRequest], None, None]:
        """
        Parse the response and extract links.

        This method extracts links from the response, yields them as LinkItems,
        and generates new requests for links that haven't been visited yet.

        Args:
            response (Response): The response to parse.

        Yields:
            Union[LinkItem, SeleniumRequest]: LinkItems for extracted links and
            SeleniumRequests for new links to visit.
        """
        if response.url not in self.links:
            self.links.add(response.url)
            yield LinkItem(link=response.url)

        yield from (
            SeleniumRequest(
                url=link.attrib["href"],
                callback=self.parse,
                wait_time=15,
                wait_until=EC.visibility_of_element_located(
                    (By.CLASS_NAME, "wrapper-conteudo-tinymce")
                ),
            )
            for link in response.css("a")
            if "href" in link.attrib
            and "pos-graduacao/programas-de-pos-graduacao/ciencia-da-computacao/"
            in link.attrib["href"]
            and link.attrib["href"] not in self.links
        )


class PageContentSpider(BaseSpider):
    """
    A spider for extracting content from specific pages.

    This spider reads a list of URLs from a file and visits each URL to extract
    page content.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): The list of allowed domains for crawling.
        start_urls (list): The list of URLs to visit, read from a file.
    """

    name = "page_content_spider"
    allowed_domains = ["www.ibilce.unesp.br"]

    def __init__(self):
        """
        Initialize the PageContentSpider.

        Reads the list of URLs from a file specified in the project settings.
        """
        links = self._read_links_file(
            links_metadata_file_path=SETTINGS.get("METADATA_FOLDER_PATH").joinpath(
                "links_metadata.csv"
            )
        )
        self.start_urls = [link[0] for link in links[1:]]

    def start_requests(self) -> Generator[SeleniumRequest]:
        """
        Generate initial requests for each URL in start_urls.

        Returns:
            Generator[SeleniumRequest]: A generator yielding SeleniumRequests for each URL.
        """

        yield from (
            SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=15,
                wait_until=EC.visibility_of_element_located(
                    (By.CLASS_NAME, "wrapper-conteudo-tinymce")
                ),
            )
            for url in self.start_urls
        )

    def parse(self, response: Response) -> Generator[PageContentItem]:
        """
        Parse the response and extract page content.

        Args:
            response (Response): The response to parse.

        Yields:
            PageContentItem: An item containing the extracted page content.
        """
        page_item = PageContentItem(
            page_name=response.css("div#idNomePagina > h2#h2NomePagina::text").get(),
            page_url=response.url,
            page_content_html=response.css("div.wrapper-conteudo-tinymce").get(),
            page_last_update=response.css(
                "div.corpo_rodape > span#data-atualizacao-pagina::text"
            ).get(),
            page_id=response.css("div.corpo_rodape > i::attr(title)").get(),
        )

        yield page_item


class ExternalContentSpider(BaseSpider):
    """
    A spider for downloading external content linked from specific pages.

    This spider reads a list of URLs from a file, visits each URL, and attempts to
    download any external content (like PDFs) linked from those pages.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): The list of allowed domains for crawling.
        start_urls (list): The list of URLs to visit, read from a file.
    """

    name = "external_content_spider"
    allowed_domains = ["www.ibilce.unesp.br"]

    def __init__(self):
        """
        Initialize the ExternalContentSpider.

        Reads the list of URLs from a file specified in the project settings.
        """
        links = self._read_links_file(
            links_metadata_file_path=SETTINGS.get("METADATA_FOLDER_PATH").joinpath(
                "links_metadata.csv"
            )
        )
        self.start_urls = [link[0] for link in links[1:]]

    def start_requests(self):
        """
        Generate initial requests for each URL in start_urls.

        Returns:
            Generator[SeleniumRequest]: A generator yielding SeleniumRequests for each URL.
        """
        yield from (
            SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=15,
                wait_until=EC.visibility_of_element_located(
                    (By.CLASS_NAME, "wrapper-conteudo-tinymce")
                ),
            )
            for url in self.start_urls
        )

    def parse(self, response: Response) -> Generator[SeleniumRequest]:
        """
        Parse the response and extract links to external content.

        Args:
            response (Response): The response to parse.

        Yields:
            SeleniumRequest: Requests for downloading external content.
        """
        base_url = f"https://{self.allowed_domains[0]}"

        if not response.css("a"):
            self.logger.info(f"No links found on page: {response.url}")
            yield ExternalContentItem()

        yield from (
            SeleniumRequest(
                url=urljoin(base_url, url),
                callback=self.parse_content,
                sleep_time=5,
                meta={
                    "external_content": ExternalContentItem(
                        file_name=url.split("/")[-1],
                        file_format=(url.split("/")[-1]).split(".")[-1],
                        file_url=urljoin(base_url, url),
                        file_origin=response.url,
                        file_download_location=Path(
                            SETTINGS.get("SELENIUM_DRIVER_EXPERIMENTAL_OPTIONS").get(
                                "download.default_directory"
                            )
                        ).joinpath(url.split("/")[-1]),
                    )
                },
            )
            for link in response.css("a")
            if "Pos-Graduacao475/CienciadaComputacao/" in (url := link.attrib["href"])
        )

    def parse_content(
        self,
        response: Response,
    ) -> Generator[ExternalContentItem]:
        """
        Parse the response for external content and attempt to download it.

        Args:
            response (Response): The response to parse.

        Yields:
            ExternalContentItem: An item containing information about the downloaded content.
        """
        external_content = response.meta["external_content"]

        if not external_content.file_download_location.is_file():
            self._download_check(
                file_download_location=external_content.file_download_location,
                timeout=25,
            )

        yield response.meta["external_content"]

    @staticmethod
    def _download_check(file_download_location: str | Path, timeout: int) -> Path:
        """
        Check if a file has been downloaded within a specified timeout period.

        Args:
            file_download_location (str | Path): The expected location of the downloaded file.
            timeout (int): The maximum time to wait for the download in seconds.

        Returns:
            Path: The resolved path of the downloaded file.

        Raises:
            FileNotFoundError: If the file is not found within the timeout period.
        """
        if not isinstance(file_download_location, Path):
            file_download_location = Path(file_download_location)
        end_time = time.time() + timeout
        while time.time() < end_time:
            if not any(
                file.suffix == ".crdownload"
                for file in file_download_location.parent.glob(
                    f"{file_download_location.stem}*"
                )
            ):
                if file_download_location.exists():
                    return file_download_location.resolve()
                break
            time.sleep(1)
        raise FileNotFoundError(
            f"File {file_download_location.resolve()} does not exist, timeout of {timeout}s reached."
        )
