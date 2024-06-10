from __future__ import annotations
import requests
from scraper.controller.vectorizer import Vectorizer
from scraper.model.scraped_website import ScrapedWebsite
from scraper.model.vectorized_website import VectorizedWebsite
from scraper.model.website import Website
from bs4 import BeautifulSoup

class WebsiteScraper:
    def __init__(self, website: Website):
        self.website = website

    def scrape_and_vectorize(self, vectorizer: Vectorizer):
        """
        Scrape and vectorize a website.

        Args:
            vectorizer (Vectorizer): The vectorizer to use for vectorization.

        Returns:
            VectorizedWebsite: The vectorized representation of the website.
        """
        scraped_website = self.scrape()
        return VectorizedWebsite(
            id=scraped_website.id,
            url=scraped_website.url,
            resource=scraped_website.resource,
            vector=vectorizer.vectorize(scraped_website)
        )

    def scrape(self):
        response = requests.get(self.website.resource)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from paragraphs
            paragraphs = soup.find_all('p')
            text = ' '.join([para.get_text() for para in paragraphs])
            return ScrapedWebsite(
                id=self.website.id,
                url=self.website.url,
                resource=self.website.resource,
                text=text
            )
        else:
            return None