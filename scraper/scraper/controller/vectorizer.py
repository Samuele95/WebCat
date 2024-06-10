from typing import Protocol, runtime_checkable
from numpy import ndarray
from scraper.model.scraped_website import ScrapedWebsite

@runtime_checkable
class Vectorizer(Protocol):
    """
    A protocol for vectorizing a scraped website.
    """

    def vectorize(self, website: ScrapedWebsite) -> list[float]:
        """
        Vectorize the given website.

        Args:
            website (ScrapedWebsite): The website to vectorize.

        Returns:
            list[float]: The vector representation of the website.
        """
        ...

    def vectorize_and_print(self, website: ScrapedWebsite) -> None:
        """
        Vectorize the given website and print the result.

        Args:
            website (ScrapedWebsite): The website to vectorize and print.
        """
        ...
