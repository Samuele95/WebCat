from collections import defaultdict
from matplotlib import pyplot as plt
from sklearn_som.som import SOM
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer, MinMaxScaler
from model.scraped_data import ScrapedData
import numpy as np

class SelfOrganizingMap:
    def __init__(self, dataset: list[ScrapedData], reduce_to_dimension: int = None, sigma: float = 1.0, learning_rate: float = 0.5):
        if dataset is None or len(dataset) == 0:
            raise ValueError('Dataset must not be null')
        self.dataset = dataset
        self.input_data = np.array([np.array(data.vector) for data in self.dataset])
        self.som_size = int(5 * np.sqrt(len(dataset)))
        self.som_plot_vertex = int(np.sqrt(self.som_size))
        self.dimension = len(self.input_data[0]) if reduce_to_dimension is None else reduce_to_dimension
        self.som = SOM(
            m=self.som_plot_vertex,
            n=self.som_plot_vertex,
            dim=self.dimension
        )
        self.clusters = defaultdict(list)
        self.predictions = np.array([])

    def fit_predict(self, reducing_algorithm, normalizer):
        self._reduce_dimensionality(algorithm=reducing_algorithm, normalizer=normalizer)
        self.predictions = self.som.fit_predict(self.input_data)
        return self

    def _reduce_dimensionality(self, algorithm, normalizer):
        reduced = make_pipeline(normalizer(), algorithm(n_components=self.dimension))
        self.input_data = reduced.fit_transform(self.input_data)
