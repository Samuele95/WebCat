from uiservice.controller.clusterer_controller import ClustererController

class ServicesInterface:
    def __init__(self, clusterer: ClustererController):
        self.clustering_service = clusterer

    @property
    def clustering_service(self):
        return self._clustering_service

    @clustering_service.setter
    def clustering_service(self, value):
        self._clustering_service = value

    @property
    def scraping_service(self):
        return self.clustering_service.clustering_client_detail.scraping_service

    @property
    def db_service(self):
        return self.scraping_service.scraper_detail.data_service

    @classmethod
    def connect(cls, db_endpoint: str, scraper_endpoint: str, clusterer_endpoint: str):
        return ServicesInterface(ClustererController.from_endpoint(
            clusterer_endpoint,
            scraper_endpoint,
            db_endpoint
        ))

    def data_as_table(self):
        return self.db_service.get_all_as_table()

    def data_from_file(self, file):
        self.db_service.from_file(file)
        return self.data_as_table()

    def website_from_id(self):
        return self.db_service.db_client.get_data_by_id()

    def add_website(self, resource: str):
        self.db_service.db_client.resource = resource
        return self.db_service.db_client.add_or_update_website()

    def update_website(self, resource: str, wid: int):
        self.db_service.db_client.resource = resource
        return self.db_service.db_client.add_or_update_website(wid=wid, update=True)

    def delete_website(self):
        return self.db_service.db_client.delete_data_by_id()

    def crawl_websites(self):
        return self.db_service.crawl_websites()

    def crawl_website(self, wid: int | None = None):
        return self.db_service.db_client.crawl_website(wid)

    def cluster_websites(self):
        return self.clustering_service.update_all()

    def website_is_present(self, wid:int | None = None):
        return self.db_service.db_client.is_present(wid)