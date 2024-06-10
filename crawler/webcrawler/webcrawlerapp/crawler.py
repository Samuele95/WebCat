from typing import Set
from urllib.parse import urlparse
from dataclasses import dataclass, field
from .models import Website
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import requests

class SimpleWebCrawler:
    def __init__(self, base_url, max_pages=50):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited = set()
        self.to_visit = [base_url]

    def fetch(self, url):
        try:
            response = requests.get(url, timeout=(5,5))
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    def parse_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for anchor in soup.find_all('a', href=True):
            link = anchor['href']
            link = urljoin(self.base_url, link)
            if self.is_valid(link):
                links.add(link)
        return links

    def is_valid(self, url):
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and parsed.netloc == urlparse(self.base_url).netloc

    def crawl(self):
        while self.to_visit and len(self.visited) < self.max_pages:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue

            print(f"Visiting: {url}")
            if html := self.fetch(url):
                self.visited.add(url)
                requests.post('http://0.0.0.0:8000/websites/', data=Website.to_dict(url))
                for link in self.parse_links(html):
                    if link not in self.visited:
                        self.to_visit.append(link)

        print(f"Crawling of {self.base_url} finished.")

