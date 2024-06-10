from __future__ import annotations
from typing import runtime_checkable, Protocol

@runtime_checkable
class ModelElement(Protocol):
    @classmethod
    def from_json(cls, json_data) -> ModelElement | None:
        ...

    def as_dict(self) -> dict:
        ...

    def as_json(self) -> str:
        ...

