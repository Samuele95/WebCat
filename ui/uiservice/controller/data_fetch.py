from __future__ import annotations
import requests
import pandas as pd
from uiservice.controller.db_client_detail import DBClientDetail
from uiservice.model.model_element import ModelElement
from uiservice.model.website import Website
from uiservice.controller.api_controller import APIController
from itertools import chain

class DataFetch(APIController):
    def __init__(self, db_client: DBClientDetail) -> None:
        self.db_client = db_client

    @property
    def db_client(self):
        return self._db_client

    @db_client.setter
    def db_client(self, value):
        self._db_client = value

    @classmethod
    def from_endpoint(cls, db_endpoint: str):
        return DataFetch(DBClientDetail(db_endpoint))


    def get_all(self) -> list[ModelElement] | None:
        try:
            response = requests.get(f'{self.db_client.db_endpoint}/')
            response.raise_for_status()
            return [Website.from_json(website) for website in response.json()]
        except requests.exceptions.Timeout:
            print(f"Timeout occurred for {self.db_client.db_endpoint}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {self.db_client.db_endpoint}: {e}")
            return None

    def get_all_as_table(self) -> pd.DataFrame:
        data = self.get_all()
        dataframe = pd.DataFrame(data) if data is None or len(data) > 0 else pd.DataFrame(
            columns=['id', 'url', 'resource', 'discovery_date', 'category'])
        dataframe['resource'] = dataframe['resource'].str[:40]
        return dataframe

    def crawl_websites(self):
        try:
            response = requests.get(f'{self.db_client.db_endpoint}/crawl/')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {self.db_client.db_endpoint}/crawl/: {e}")
            return None


    def from_file(self, file) -> None:
        data = pd.read_csv(file, sep=" ", header=None).to_dict('list')
        for element in chain.from_iterable(data.values()):
            try:
                response = requests.post(f'{self.db_client.db_endpoint}/', json={'resource': element})
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error inserting element in DB: {e}")