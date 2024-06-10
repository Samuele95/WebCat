from typing import runtime_checkable, Protocol
from uiservice.model.model_element import ModelElement
import pandas as pd

@runtime_checkable
class ControllerElement(Protocol):
    def get_all(self) -> list[ModelElement] | None:
        ...

    def get_all_as_table(self) -> pd.DataFrame:
        ...

    def get_data_by_id(self, wid: int) -> ModelElement | None:
        ...

    def is_present(self, wid: int) -> bool:
        ...
