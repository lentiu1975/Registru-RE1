from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import ManifestEntry
from .serializers import ManifestEntrySerializer, ManifestSearchSerializer


class ManifestEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pentru cautare si vizualizare intrari manifest.
    Doar utilizatorii autentificati pot accesa.
    """
    queryset = ManifestEntry.objects.all()
    serializer_class = ManifestEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numar_manifest', 'container', 'model_container', 'nume_nava']
    ordering_fields = ['data_inregistrare', 'created_at', 'numar_manifest']
    ordering = ['-data_inregistrare']

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Endpoint custom pentru cautare dupa container si/sau numar_manifest
        GET /api/manifests/search/?container=XXX&numar_manifest=YYY
        """
        serializer = ManifestSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        container = serializer.validated_data.get('container', '').strip()
        numar_manifest = serializer.validated_data.get('numar_manifest', '').strip()

        queryset = self.get_queryset()

        # Filtru dupa container (exact sau partial)
        if container:
            queryset = queryset.filter(
                Q(container__icontains=container) |
                Q(model_container__icontains=container)
            )

        # Filtru dupa numar manifest (exact sau partial)
        if numar_manifest:
            queryset = queryset.filter(numar_manifest__icontains=numar_manifest)

        # Paginare
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
