from typing import runtime_checkable, Any
#import tensorflow as tf
#import tensorflow_hub as hub
#import tensorflow_text as text
from keybert import KeyBERT
from scraper.model.scraped_website import ScrapedWebsite


class KeyBERTTokenizer:
    """
    A class to tokenize text using the BERT model from TensorFlow Hub.
    """

    def __init__(self):
        self._model = KeyBERT()

    def tokenize_text(self, website: ScrapedWebsite):
        """
        Tokenize the text of a scraped website using BERT tokenizer.

        Args:
            website (ScrapedWebsite): The scraped website object containing text to tokenize.

        Returns:
            dict: BERT inputs after tokenization.
        """
        # Use the BERT tokenizer from TensorFlow Hub to preprocess the input text
        keywords_tuples = self._model.extract_keywords(website.text)
        #kwords, distances = list(map(list, zip(*keywords_tuples)))
        #print("BERT Inputs:", bert_inputs)
        return [kword for kword, dist in keywords_tuples] , [], []


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