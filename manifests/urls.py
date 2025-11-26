from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManifestEntryViewSet

router = DefaultRouter()
router.register(r'manifests', ManifestEntryViewSet, basename='manifest')

urlpatterns = [
    path('', include(router.urls)),
]
