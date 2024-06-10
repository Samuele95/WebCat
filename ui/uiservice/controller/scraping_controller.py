from concurrent.futures import ThreadPoolExecutor
from uiservice.controller.data_fetch import DataFetch
from uiservice.controller.scraping_detail import ScrapingDetail
from uiservice.model.model_element import ModelElement
from uiservice.model.scraped_data import ScrapedData
from uiservice.model.website import Website
from uiservice.controller.api_controller import APIController
import requests
import pandas as pd


class ScrapingController(APIController):
    def __init__(self, scraper_detail: ScrapingDetail) -> None:
        self.scraper_detail = scraper_detail

    @classmethod
    def from_endpoint(cls, scraper_endpoint: str, db_endpoint: str):
        return ScrapingController(ScrapingDetail(
            scraper_endpoint=scraper_endpoint,
            data_service=DataFetch.from_endpoint(db_endpoint)
        ))


    def get_all(self) -> list[ModelElement] | None:
        try:
            website_list = self.scraper_detail.data_service.get_all()
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.scraper_detail.get_data_by_id, website.id) for website in website_list]
            return [future.result() for future in futures]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {self.scraper_detail.scraper_endpoint}: {e}")
            return None
        except AttributeError as e:
            print(f"No data available")
            return None

    def get_all_as_table(self) -> pd.DataFrame:
        return pd.DataFrame(self.get_all())
