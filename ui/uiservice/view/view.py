from typing import runtime_checkable, Protocol


@runtime_checkable
class View(Protocol):
    def open(self, show_logo: bool = True) -> None:
        ...

    def close(self) -> None:
        ...

