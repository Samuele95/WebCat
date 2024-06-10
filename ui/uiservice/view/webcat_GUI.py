from solara.tasks import task
from concurrent.futures import ThreadPoolExecutor
from uiservice.controller.clusterer_controller import ClustererController
from uiservice.controller.data_fetch import DataFetch
from uiservice.controller.scraping_controller import ScrapingController
from uiservice.controller.services_interface import ServicesInterface
from matplotlib.figure import Figure
from pathlib import Path
from time import sleep
import numpy as np
import pandas as pd
import datetime as dt
import solara
import solara.lab
import math
import sys
import requests

#----------------------------------------------------------------------
#---------------- GENERAL SERVICES AND ASYNC TASKS --------------------
#----------------------------------------------------------------------


services_interface = ServicesInterface.connect(
    'http://webcrawler:8000/websites',
    'http://scraper:5000/scraper/',
    'http://clusterer:6000/clusterer'
)


@solara.component
def Page():
    return WebCatGUI(services_interface).open()

@solara.component
def Layout(children):
    return solara.AppLayout(children=children, title='WebCat')

@task
def crawl_website():
    return services_interface.crawl_website()

@task
def crawl_websites():
    return services_interface.crawl_websites()

@task
def cluster_websites():
    return services_interface.cluster_websites()

@task
def load_from_file(file):
    return services_interface.data_from_file(file["file_obj"])

#----------------------------------------------------------------------
#------------------------ SOLARA VIEW CLASS ---------------------------
#----------------------------------------------------------------------

class WebCatGUI:
    def __init__(self, services_interface):
        self.services_interface = services_interface
        self.wid, self.set_wid = solara.use_state(1)
        self._get_data(init=True)
        self.resource, self.set_resource = solara.use_state('')
        self.plot_input_data, self.set_plot_input_data = solara.use_state(services_interface.clustering_service.input_data)
        self.plot_predictions, self.set_plot_predictions = solara.use_state(services_interface.clustering_service.predictions)

    def open(self, show_logo: bool = True) -> None:
        self.MainPage()

    def close(self) -> None:
        return sys.exit(0)

    def MainPage(self):
        with solara.Sidebar():
            solara.Image(Path(__file__).parent / 'webcat.png', width='100%')
            self._crawl_websites()
            self._cluster_websites()
            self._add_websites()
        with solara.VBox():
            with solara.ColumnsResponsive():
                self._websites()
                self._website_by_id()
            self._charts()

    def _set_wid(self, wid:int):
        self.services_interface.db_service.db_client.wid = wid

    def _set_reducing_algorithm(self, reducing_algorithm: str):
        self.services_interface.clustering_service.reducing_algorithm = reducing_algorithm

    def _set_normalizer(self, normalizer: str):
        self.services_interface.clustering_service.normalizer = normalizer


    def _get_data(self, init: bool = False):
        data = self.services_interface.data_as_table()
        dataframe = data if len(data) > 0 else pd.DataFrame(columns=['id', 'url', 'resource', 'discovery_date', 'category'])
        if init:
            self.data, self.set_data = solara.use_state(dataframe)
            self.website, self.set_website = solara.use_state(self.services_interface.website_from_id() if len(dataframe) > 0 else None)
            return
        self.set_data(dataframe)
        self.set_website(self.services_interface.website_from_id() if len(dataframe) > 0 else None)


    def _websites(self):
        with solara.Card("Websites"):
            solara.provide_cross_filter()
            dataframe = self.data.drop(['url'], axis=1)
            if len(dataframe) > 0:
                solara.CrossFilterReport(dataframe, classes=["py-2"])
                solara.CrossFilterSelect(dataframe, "category")
            solara.CrossFilterDataFrame(dataframe, items_per_page=10)

    def _retrieve_website_data(self, wid: int):
        self.services_interface.db_service.db_client.wid = wid if self.services_interface.website_is_present(wid) else 1
        self.set_website(self.services_interface.website_from_id())

    def _website_by_id(self):
        with solara.Card("Info about", margin=0, elevation=0):
            if self.data is None or len(self.data) == 0:
                solara.Text(text='No data available')
            else:
                if self.website is None:
                    self._retrieve_website_data(wid=1)
                with solara.VBox():
                    solara.InputInt("ID", value=self.website.id, on_value=self._retrieve_website_data,
                                    continuous_update=True)
                    solara.Text(text=f'URL: {self.website.resource}')
                    solara.Text(text=f'Discovery Date: {self.website.discovery_date}')
                    solara.Text(text=f'Category: {self.website.category}')
                    solara.Button('Crawl website', color='green', outlined=True, text=True,
                                on_click=crawl_website)
                    solara.ProgressLinear(crawl_website.pending)
                    if crawl_website.finished:
                        self._refresh_data()
                    elif crawl_website.not_called:
                        solara.Text("Click the button to start crawling from this website")
                    solara.Button('Delete website', color='red', outlined=True, text=True,
                                on_click=self._delete_website_from_table)

    def _crawl_websites(self):
        with solara.Card():
            with solara.VBox():
                solara.Button('Start crawling', color='green', outlined=True, on_click=crawl_websites)
                solara.ProgressLinear(crawl_websites.pending)
                if crawl_websites.finished:
                    self._refresh_data()
                elif crawl_websites.not_called:
                    solara.Text("Click the button to crawl more websites from the ones stored in the database")
    def _cluster_websites(self):
        with solara.Card():
            with solara.VBox():
                solara.Button('Start clustering', color='green', outlined=True, on_click=cluster_websites)
                solara.Select(label='With dimensionality reduction algorithm', value='LSA', values=['LSA', 'PCA'], on_value=self._set_reducing_algorithm)
                solara.Select(label='With normalizer algorithm', value='MinMaxScaler', values=['MinMaxScaler', 'StandardScaler', 'Unit-Norm-Normalizer'], on_value=self._set_normalizer)
                solara.ProgressLinear(cluster_websites.pending)
                if cluster_websites.finished:
                    self._refresh_data()
                elif cluster_websites.not_called:
                    solara.Text("Click the button to cluster the given websites")

    def _refresh_data(self):
        self._get_data()
        self.set_plot_input_data(self.services_interface.clustering_service.input_data)
        self.set_plot_predictions(self.services_interface.clustering_service.predictions)

    def _add_websites(self):
        with solara.Card('Add new websites', margin=0, elevation=0):
            with solara.VBox():
                with solara.Card('From file'):
                    solara.FileDrop(label='Drop a .txt or .csv file here', on_file=load_from_file)
                    solara.ProgressLinear(load_from_file.pending)
                    if load_from_file.finished:
                        self.set_data(load_from_file.value)
                        self._refresh_data()
                with solara.Card("Through form"):
                    with solara.VBox():
                        solara.InputText(label='Website URL', on_value=self.set_resource,
                                         continuous_update=True)
                        solara.Button('Add website', color='blue', outlined=True,
                                      on_click=self._add_website_to_table)

    def _add_website_to_table(self):
        self.services_interface.add_website(self.resource)
        self._get_data()

    def _delete_website_from_table(self):
        self.services_interface.delete_website()
        self._get_data()

    def _charts(self):
        with solara.Card("Last SOM output"):
            with solara.ColumnsResponsive():
                self._plot_clusters()

    def _plot_clusters(self):
        fig = Figure(figsize=(16, 16))
        ax = fig.subplots()
        x = self.plot_input_data[:, 0] if len(self.plot_input_data) != 0 else self.plot_input_data
        y = self.plot_input_data[:, 1] if len(self.plot_input_data) != 0 else x
        ax.scatter(x, y, c=self.plot_predictions, cmap='viridis')
        ax.title.set_text('SOM Predictions')
        return solara.FigureMatplotlib(fig, dependencies=[self.plot_input_data, self.plot_predictions])
