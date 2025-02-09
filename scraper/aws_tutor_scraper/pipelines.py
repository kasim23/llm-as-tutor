# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import weaviate
import openai
from dotenv import load_dotenv
import logging
from datetime import datetime


class AwsTutorScraperPipeline:
    def process_item(self, item, spider):
        return item


class WeaviatePipeline:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '../../backend/.env'))
        self.vector_db_url = os.getenv("VECTOR_DB_URL")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
        self.client = weaviate.Client(self.vector_db_url)
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        """
        Process each scraped item: generate embedding and store in Weaviate.
        """
        try:
            # Generate embedding
            embedding = self.generate_embedding(item['content'])
            if not embedding:
                self.logger.error(f"Embedding generation failed for URL: {item['url']}")
                return item

            # Store in Weaviate
            self.store_embedding(item, embedding)
            self.logger.info(f"Stored data for URL: {item['url']}")
        except Exception as e:
            self.logger.error(f"Error processing item: {e}")
        return item

    def generate_embedding(self, text):
        """
        Generate embedding using OpenAI's API.
        """
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response['data'][0]['embedding']
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return None

    def store_embedding(self, item, embedding):
        """
        Store the content and its embedding in Weaviate.
        """
        try:
            self.client.data_object.create(
                {
                    "title": item['title'],
                    "content": item['content'],
                    "url": item['url'],
                    "section": item['section'],
                    "timestamp": item['timestamp'],
                    "source": "AWS Documentation"
                },
                "AWSDocument",
                vector=embedding
            )
        except Exception as e:
            self.logger.error(f"Weaviate storage error: {e}")
