import json
from dataclasses import dataclass
from datetime import datetime
from model.model_element import ModelElement


@dataclass(frozen=True, eq=True, order=True)
class Website:
    id: int
    url: str
    resource: str
    discovery_date: datetime | None = None
    category: int | None = None

    @classmethod
    def from_json(cls, json_data) -> ModelElement | None:
        try:
            return Website(**json_data)
        except (TypeError,KeyError):
            print('Wrong data format from DB Api. Closing app.')
            return None

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'url': self.url,
            'resource': self.resource,
            'discovery_date': self.discovery_date,
            'category': self.category
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())

    def __str__(self) -> str:
        return f'''
        Website information:
        Resource: {self.resource}
        Discovery Date: {self.discovery_date}
        Category: {self.category} 
        '''
