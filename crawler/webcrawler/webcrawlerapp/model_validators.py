from rest_framework import serializers
from .models import Website


class WebsiteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Website serialization class for field validation purposes.
    """

    class Meta:
        model = Website
        fields = ['id','url', 'resource', 'discovery_date', 'category']
