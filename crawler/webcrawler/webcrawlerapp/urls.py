from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import WebsiteViewSet

# Create a router and register viewsets with it.
router = DefaultRouter()
router.register(r'websites', WebsiteViewSet, basename="website")

# The API URLs are determined automatically by the router.
urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(r'', include(router.urls)),
]
