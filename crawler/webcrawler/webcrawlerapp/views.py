import json

from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from concurrent.futures import ThreadPoolExecutor
from .crawler import SimpleWebCrawler
from .models import Website
from .model_validators import WebsiteSerializer
#from scrapy.crawler import CrawlerProcess

from .pagination import Unpaginatable


class WebsiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint allowing websites to be viewed or edited.
    """
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    pagination_class = Unpaginatable

    @action(
        detail=False,
        methods=['get'],
        url_path=r'new'
    )
    def get_unclustered_websites(self, request):
        """
        Custom action to get unclustered websites.

        Args:
            request: The request object.

        Returns:
            Response: Response with unclustered websites.
        """
        try:
            return Response(self.serializer_class(
                Website.objects.filter(category=None),
                many=True,
                context={'request': request}).data)
        except Website.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=False,
        methods=['get'],
        url_path=r'crawl',
    )
    def crawl_all_websites(self, request):
        """
        Custom action to crawl a website.

        Args:
            request: The request object.

        Returns:
            Response: Empty response.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(SimpleWebCrawler(website.resource, max_pages=10).crawl) for website in Website.objects.all()]
        futures = [future.result() for future in futures]
        return Response()

    @action(
        detail=True,
        methods=['get'],
        url_path=r'crawl',
    )
    def crawl_website(self, request, *args, **kwargs):
        SimpleWebCrawler(self.get_object().resource, max_pages=10).crawl()
        return Response()


