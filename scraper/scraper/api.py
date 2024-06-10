from __future__ import annotations
from flask import Flask, request, jsonify
from flask_restx import Resource, Api
import sys

from scraper.controller.bert_tokenizer import BERTTokenizer
from scraper.controller.bert_vectorizer import BERTVectorizer
from scraper.controller.website_scraper import WebsiteScraper
from scraper.model.website import Website

from scraper.controller.key_bert_tokenizer import KeyBERTTokenizer

app = Flask(__name__)
api = Api(app)
tokenizer = BERTTokenizer()
vectorizer = BERTVectorizer(tokenizer=tokenizer)

@api.route('/scraper/', methods=['POST'])
@api.response(404, 'Website not found for scraping')
class WebsiteTextProcessor(Resource):
    """
    Resource for processing website text using BERT tokenizer and vectorizer.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        """
        POST method for processing website text.

        Returns:
            dict: Vectorized representation of the website text.
        """
        try:
            if request.is_json:
                data = request.json
                return WebsiteScraper(website=Website(
                        id=data.get('id'),
                        url=data.get('url'),
                        resource=data.get('resource')
                )).scrape_and_vectorize(vectorizer=vectorizer).as_dict()
            print('Some error occurred in receiving data for request')
            return None
        except Exception as e:
            print(jsonify({'error': str(e)}), 500)


if __name__ == '__main__':
    app.config['source_endpoint'] = sys.argv[1] if len(sys.argv) > 1 else 'http://webcrawler:8000/websites/'
    app.config['host'] = sys.argv[2] if len(sys.argv) > 2 else '0.0.0.0'
    app.config['port'] = sys.argv[3] if len(sys.argv) > 3 else '5000'
    app.run(host='0.0.0.0', port='5000', debug=True)

