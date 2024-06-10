from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer, MinMaxScaler, StandardScaler
from flask import Flask, request, jsonify, send_file
from flask_restx import Resource, Api, abort
from model.som import SelfOrganizingMap
from model.website import Website
from model.scraped_data import ScrapedData
from pathlib import Path
import numpy as np
import sys
import json
import os

app = Flask(__name__)
api = Api(app)


@api.route('/clusterer/', defaults={'reducing_algorithm': 'LSA', 'normalizer': 'MinMaxScaler'}, methods=['POST'])
@api.route('/clusterer/<reducing_algorithm>/', defaults={'normalizer': 'MinMaxScaler'}, methods=['POST'])
@api.route('/clusterer/<reducing_algorithm>/<normalizer>/', methods=['POST'])
@api.response(404, 'Clusterer service not found')
class WebsiteClusterer(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, reducing_algorithm, normalizer):
        try:
            if request.is_json:
                data = [ScrapedData.from_json(resource) for resource in request.json]
                som = SelfOrganizingMap(dataset=data, reduce_to_dimension=2)
                som.fit_predict(
                    reducing_algorithm=self._reducing_algorithm(reducing_algorithm),
                    normalizer=self._normalizer(normalizer)
                )
                return {
                    'results': [Website(
                        id=scraped_website.id,
                        url=scraped_website.url,
                        resource=scraped_website.resource,
                        category=int(cluster)).as_dict() for (scraped_website, cluster) in zip(data, som.predictions)],
                    'input_data': som.input_data.tolist(),
                    'predictions': som.predictions.tolist()
                }
            return None
        except Exception as e:
            print(jsonify({'error': str(e)}), 500)

    def _reducing_algorithm(self, reducing_algorithm: str):
        match reducing_algorithm:
            case 'PCA':
                return PCA
            case _:
                return TruncatedSVD

    def _normalizer(self, normalizer: str):
        match normalizer:
            case 'Unit-Norm-Normalizer':
                return Normalizer
            case 'StandardScaler':
                return StandardScaler
            case _:
                return MinMaxScaler



if __name__ == '__main__':
    app.config['host'] = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    app.config['port'] = sys.argv[2] if len(sys.argv) > 2 else '6000'
    app.run(host='0.0.0.0', port='6000', debug=True)
