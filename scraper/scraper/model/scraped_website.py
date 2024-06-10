import json
import re
from dataclasses import dataclass, field
from scraper.model.model_element import ModelElement

@dataclass(frozen=True, eq=True, order=True)
class ScrapedWebsite:
    id: int
    url: str
    resource: str
    text: str

    @classmethod
    def from_json(cls, json_data) -> ModelElement | None:
        try:
            return ScrapedWebsite(**json_data)
        except (TypeError,KeyError):
            print('Wrong data format from DB Api. Closing app.')
            return None

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'url': self.url,
            'resource': self.resource,
            'text': self.text
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())

