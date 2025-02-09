import scrapy
from aws_tutor_scraper.items import AwsTutorScraperItem
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
from datetime import datetime

class AwsDocsSpider(scrapy.Spider):
    name = "aws_docs"
    allowed_domains = ["docs.aws.amazon.com"]
    start_urls = ["https://docs.aws.amazon.com/"]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # 1-second delay between requests
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'ROBOTSTXT_OBEY': True,
    }

    def parse(self, response):
        """
        Parse the homepage and extract internal links to follow.
        """
        internal_links = response.css("a::attr(href)").getall()
        for link in internal_links:
            link = link.strip()
            if not link.startswith("http"):
                link = urljoin(response.url, link)
            if re.match(r"https://docs\.aws\.amazon\.com/.+", link):
                yield scrapy.Request(url=link, callback=self.parse_docs)
    
    def parse_docs(self, response):
        """
        Parse individual documentation pages and extract content.
        """
        item = AwsTutorScraperItem()
        item['title'] = response.css("title::text").get().strip()
        # Adjust the selector based on AWS docs structure
        content_div = response.css("div.main-content").get() or response.css("article").get()
        if content_div:
            # Clean and extract text
            soup = BeautifulSoup(content_div, 'html.parser')
            text = soup.get_text(separator="\n", strip=True)
            item['content'] = text
            item['url'] = response.url
            item['section'] = self.extract_section(soup)
            item['timestamp'] = datetime.utcnow().isoformat()
            yield item

            # Recursively follow internal links within the page
            internal_links = response.css("a::attr(href)").getall()
            for link in internal_links:
                link = link.strip()
                if not link.startswith("http"):
                    link = urljoin(response.url, link)
                if re.match(r"https://docs\.aws\.amazon\.com/.+", link):
                    yield scrapy.Request(url=link, callback=self.parse_docs)

    def extract_section(self, soup):
        """
        Extract the current section or heading for metadata.
        """
        # Example: Extract h1 or h2 tags
        section = soup.find(['h1', 'h2'])
        return section.get_text().strip() if section else ""
