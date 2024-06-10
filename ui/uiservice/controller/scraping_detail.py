from uiservice.controller.data_fetch import DataFetch
from uiservice.model.model_element import ModelElement
from uiservice.model.scraped_data import ScrapedData
import requests

class ScrapingDetail:
    def __init__(self, scraper_endpoint: str, data_service: DataFetch) -> None:
        self.scraper_endpoint = scraper_endpoint
        self.data_service = data_service

    def get_data_by_id(self, wid: int) -> ModelElement | None:
        try:
            website = self.data_service.db_client.get_data_by_id(wid)
            response = requests.post(f'{self.scraper_endpoint}', json=website.as_dict(), timeout=(5,5))
            response.raise_for_status()
            return ScrapedData.from_json(response.json())
        except requests.exceptions.Timeout:
            print(f"Timeout occurred for {self.scraper_endpoint}{wid}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {self.scraper_endpoint}/{wid}: {e}")
            return None