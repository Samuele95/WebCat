import json
from dataclasses import dataclass
from uiservice.model.model_element import ModelElement


@dataclass(frozen=True, eq=True, order=True)
class ScrapedData:
    id: int
    url: str
    resource: str
    vector: list[float]

    @classmethod
    def from_json(cls, json_data) -> ModelElement | None:
        try:
            return ScrapedData(**json_data)
        except (TypeError,KeyError):
            print('Wrong data format from Scraping Service Api. Closing app.')
            return None

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'url': self.url,
            'resource': self.resource,
            'vector': self.vector
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())