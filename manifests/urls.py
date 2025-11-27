from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ManifestEntryViewSet, DatabaseYearViewSet, ContainerTypeViewSet,
    ShipViewSet, PavilionViewSet, get_csrf_token, login_view, logout_view, check_auth_view,
    latest_manifest_view
)

router = DefaultRouter()
router.register(r'manifests', ManifestEntryViewSet, basename='manifest')
router.register(r'years', DatabaseYearViewSet, basename='databaseyear')
router.register(r'container-types', ContainerTypeViewSet, basename='containertype')
router.register(r'ships', ShipViewSet, basename='ship')
router.register(r'pavilions', PavilionViewSet, basename='pavilion')

urlpatterns = [
    path('csrf/', get_csrf_token, name='csrf'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('check-auth/', check_auth_view, name='check_auth'),
    path('latest-manifest/', latest_manifest_view, name='latest_manifest'),
    path('', include(router.urls)),
]
