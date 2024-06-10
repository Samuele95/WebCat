from __future__ import annotations
import requests
import pandas as pd
from uiservice.model.model_element import ModelElement
from uiservice.model.website import Website
from uiservice.controller.api_controller import APIController

class DBClientDetail:
    def __init__(self, db_endpoint: str, wid: int = 1, resource: str | None = None, category: int | None = None):
        self.db_endpoint = db_endpoint
        self.wid = wid
        self.resource = resource
        self.category = category

    @property
    def db_endpoint(self):
        return self._db_endpoint

    @db_endpoint.setter
    def db_endpoint(self, value):
        self._db_endpoint = value

    @property
    def wid(self):
        return self._wid

    @wid.setter
    def wid(self, value):
        self._wid = value if value >= 1 else 1

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, value):
        self._resource = value

    def get_data_by_id(self, wid: int | None = None) -> ModelElement | None:
        try:
            wid = self.wid if wid is None else wid
            response = requests.get(f'{self.db_endpoint}/{wid}/', timeout=(5,5))
            response.raise_for_status()
            return Website.from_json(response.json())
        except requests.exceptions.Timeout:
            print(f"Timeout occurred for {self.db_endpoint}/{self.wid}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {self.db_endpoint}/{wid}: {e}")
            return None

    def crawl_website(self, wid: int | None = None):
        wid = self.wid if wid is None else wid
        if self.is_present(wid):
            requests.get(f'{self.db_endpoint}/{wid}/crawl/')
    def is_present(self, wid: int | None = None) -> bool:
        wid = self.wid if wid is None else wid
        return self.get_data_by_id(wid) is not None

    def add_or_update_website(self, wid: int | None = None, update: bool = False) -> DBClientDetail | None:
        try:
            wid = self.wid if wid is None else wid
            data = {'resource': self.resource}
            if self.category is not None:
                data['category'] = self.category
            if not update:
                response = requests.post(f'{self.db_endpoint}/', json=data)
            else:
                response = requests.put(f'{self.db_endpoint}/{wid}/', json=data)
            response.raise_for_status()
            print('Website added successfully!')
            return self
        except requests.HTTPError as ex:
            print('Some error occurred during website creation or update')
            return None

    def delete_data_by_id(self, wid: int | None = None) -> None:
        try:
            if not self.db_endpoint:
                return print('No resource to delete')
            wid = self.wid if wid is None else wid
            response = requests.delete(f'{self.db_endpoint}/{wid}/')
            response.raise_for_status()
            print('Element correctly deleted')
            self.wid = 1
        except requests.HTTPError as ex:
            return print(str(ex))