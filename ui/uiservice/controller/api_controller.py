from abc import ABC
from uiservice.model.model_element import ModelElement
import pandas as pd

class APIController(ABC):
    def get_all(self) -> list[ModelElement] | None:
        pass

    def get_all_as_table(self) -> pd.DataFrame:
        pass

    def get_data_by_id(self, wid: int) -> ModelElement | None:
        pass
