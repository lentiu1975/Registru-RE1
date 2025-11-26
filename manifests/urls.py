from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManifestEntryViewSet, get_csrf_token

router = DefaultRouter()
router.register(r'manifests', ManifestEntryViewSet, basename='manifest')

urlpatterns = [
    path('csrf/', get_csrf_token, name='csrf'),
    path('', include(router.urls)),
]
