from typing import runtime_checkable, Any
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text

from scraper.model.scraped_website import ScrapedWebsite
from scraper.controller.tokenizer import Tokenizer


class BERTTokenizer:
    """
    A class to tokenize text using the BERT model from TensorFlow Hub.
    """

    def __init__(self, preprocessor_tokenizer: Tokenizer | None = None):
        self._model = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
        self.preprocessor_tokenizer = preprocessor_tokenizer

    def tokenize_text(self, website: ScrapedWebsite):
        """
        Tokenize the text of a scraped website using BERT tokenizer.

        Args:
            website (ScrapedWebsite): The scraped website object containing text to tokenize.

        Returns:
            dict: BERT inputs after tokenization.
        """
        # Use the BERT tokenizer from TensorFlow Hub to preprocess the input text
        processed_text = website.text
        if self.preprocessor_tokenizer is not None:
            preprocessor_output, some_data, other = self.preprocessor_tokenizer.tokenize_text(website)
            processed_text = ' '.join(preprocessor_output)
        bert_inputs = self._model(tf.constant([processed_text]))
        print("BERT Inputs:", bert_inputs)
        return bert_inputs

    @property
    def model(self):
        """
        Get the BERT model.

        Returns:
            Any: The BERT model.
        """
        return self._model

    @model.setter
    def model(self, value):
        """
        Set the BERT model.

        Args:
            value (Any): The BERT model to set.
        """
        self._model = value

