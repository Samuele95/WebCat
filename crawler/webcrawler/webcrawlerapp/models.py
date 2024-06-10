from django.db import models


class Website(models.Model):
    """
    Model representing a website.
    """

    resource = models.URLField()
    discovery_date = models.DateField(auto_now=True)
    category = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = '1. Websites'

    @classmethod
    def to_dict(cls, resource, discovery_date=None, category=None):
        """
        Convert model fields to a dictionary.

        Args:
            resource: The resource field value.
            discovery_date: The discovery_date field value.
            category: The category field value.

        Returns:
            dict: A dictionary representation of the model.
        """
        json_data = {'resource': resource}
        if discovery_date is not None:
            json_data['discovery_date'] = discovery_date
        if category is not None:
            json_data['category'] = category
        return json_data

    def __str__(self) -> str:
        """
        String representation of the Website object.

        Returns:
            str: The string representation of the resource field.
        """
        return str(self.resource)

