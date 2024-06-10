from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd
import requests

from uiservice.controller.clustering_client_detail import ClusteringClientDetail
from uiservice.controller.scraping_controller import ScrapingController
from uiservice.model.model_element import ModelElement
from uiservice.model.website import Website
from uiservice.controller.api_controller import APIController


class ClustererController(APIController):
    def __init__(self, clustering_client_detail: ClusteringClientDetail, reducing_algorithm: str = 'LSA', normalizer: str = 'MinMaxScaler') -> None:
        self.clustering_client_detail = clustering_client_detail
        self.input_data = np.array([])
        self.predictions = np.array([])
        self.reducing_algorithm = reducing_algorithm
        self.normalizer = normalizer

    @classmethod
    def from_endpoint(cls, clusterer_endpoint: str, scraper_endpoint: str, db_endpoint: str):
        return ClustererController(ClusteringClientDetail(
            clusterer_endpoint=clusterer_endpoint,
            scraping_service=ScrapingController.from_endpoint(
                scraper_endpoint=scraper_endpoint,
                db_endpoint=db_endpoint
            )
        ))

    def get_all(self) -> list[ModelElement] | None:
        try:
            website_list = [element.as_dict() for element in self.clustering_client_detail.scraping_service.get_all() if element is not None]
            response = requests.post(f'{self.clustering_client_detail.clusterer_endpoint}/{self.reducing_algorithm}/{self.normalizer}/', json=website_list)
            response.raise_for_status()
            self.input_data = np.array(response.json()['input_data'])
            self.predictions = np.array(response.json()['predictions'])
            return [Website.from_json(website) for website in response.json()['results']]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {self.clustering_client_detail.clusterer_endpoint}: {e}")
            return None

    def get_all_as_table(self) -> pd.DataFrame:
        return pd.DataFrame(self.get_all())


    def update_all(self):
        for website in self.get_all():
            db_client = self.clustering_client_detail.scraping_service.scraper_detail.data_service.db_client
            db_client.wid = website.id
            db_client.resource = website.resource
            db_client.category = website.category
            db_client.add_or_update_website(update=True)
