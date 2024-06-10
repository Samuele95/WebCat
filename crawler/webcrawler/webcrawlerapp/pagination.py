from rest_framework.pagination import PageNumberPagination


class Unpaginatable(PageNumberPagination):
    """
    A custom pagination class that prevents pagination if 'page' query parameter is not provided.
    """

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate queryset if 'page' query parameter is provided.

        Args:
            queryset: The queryset to paginate.
            request: The request object.
            view: The view object.

        Returns:
            queryset or None: The paginated queryset if 'page' query parameter is provided, else None.
        """
        if 'page' not in request.query_params:
            return None
        return super().paginate_queryset(queryset, request, view)
