from numpy import ndarray
import tensorflow_hub as hub
import tensorflow as tf
from scraper.model.scraped_website import ScrapedWebsite
from scraper.controller.tokenizer import Tokenizer

class BERTVectorizer:
    """
    A class to vectorize website text using BERT embeddings.

    Attributes:
        model (KerasLayer): A TensorFlow Hub Keras Layer for BERT.
        tokenizer (Tokenizer): A tokenizer to preprocess the website text.
    """

    def __init__(self, tokenizer: Tokenizer):
        """
        Initialize the BERTVectorizer with a tokenizer.

        Args:
            tokenizer (Tokenizer): The tokenizer to preprocess the website text.
        """
        self._model = hub.KerasLayer(
            "https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-512_A-8/2",
            trainable=False)
        self._tokenizer = tokenizer

    @property
    def model(self):
        """
        Get the BERT model.

        Returns:
            KerasLayer: The BERT model.
        """
        return self._model

    @model.setter
    def model(self, value):
        """
        Set the BERT model.

        Args:
            value (KerasLayer): The new BERT model.
        """
        self._model = value

    @property
    def tokenizer(self):
        """
        Get the tokenizer.

        Returns:
            Tokenizer: The tokenizer.
        """
        return self._tokenizer

    @tokenizer.setter
    def tokenizer(self, value):
        """
        Set the tokenizer.

        Args:
            value (Tokenizer): The new tokenizer.
        """
        self._tokenizer = value

    def vectorize(self, website: ScrapedWebsite) -> list[float]:
        """
        Get the BERT vector representation of the website text.

        Args:
            website (ScrapedWebsite): The website to vectorize.

        Returns:
            list[float]: The BERT vector representation of the website text.
        """
        return self.model(self.tokenizer.tokenize_text(website))["pooled_output"].numpy().tolist()[0]

    def vectorize_and_print(self, website: ScrapedWebsite) -> None:
        """
        Vectorize the website text and print the BERT vector.

        Args:
            website (ScrapedWebsite): The website to vectorize and print.
        """
        print("Text:", website.text)
        print("BERT Vector:", self.vectorize(website))

