from typing import runtime_checkable, Tuple, Any, Protocol
from scraper.model.scraped_website import ScrapedWebsite


@runtime_checkable
class Tokenizer(Protocol):
    """
    A protocol for tokenizing the text of a scraped website.
    """

    def tokenize_text(self, website: ScrapedWebsite) -> Tuple[Any, Any, Any]:
        """
        Tokenize the text of the given website.

        Args:
            website (ScrapedWebsite): The website whose text is to be tokenized.

        Returns:
            Tuple[Any, Any, Any]: The tokenized representation of the website's text.
        """
        ...




