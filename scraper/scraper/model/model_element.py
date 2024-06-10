from __future__ import annotations
from typing import runtime_checkable, Protocol

@runtime_checkable
class ModelElement(Protocol):
    """
    A protocol defining the structure for model elements that can be serialized to and from JSON.
    """

    @classmethod
    def from_json(cls, json_data) -> ModelElement | None:
        """
        Create an instance of the model element from a JSON object.
        
        Args:
            json_data (dict): A dictionary representing the JSON data.

        Returns:
            ModelElement | None: An instance of the model element or None if creation fails.
        """
        ...

    def as_dict(self) -> dict:
        """
        Convert the model element to a dictionary.
        
        Returns:
            dict: A dictionary representation of the model element.
        """
        ...

    def as_json(self) -> str:
        """
        Convert the model element to a JSON string.
        
        Returns:
            str: A JSON string representation of the model element.
        """
        ...

