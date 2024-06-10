import pandas as pd
import requests

from uiservice.controller.scraping_controller import ScrapingController
from uiservice.model.model_element import ModelElement
from uiservice.model.website import Website
from uiservice.controller.api_controller import APIController

class ClusteringClientDetail:
    def __init__(self, clusterer_endpoint: str, scraping_service: ScrapingController):
        self.clusterer_endpoint = clusterer_endpoint
        self.scraping_service = scraping_service

    def get_data_by_id(self, wid: int) -> ModelElement | None:
        return None