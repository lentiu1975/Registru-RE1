from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Max
from .models import ManifestEntry, DatabaseYear, ContainerType, Ship, Pavilion
from .serializers import (
    ManifestEntrySerializer, ManifestSearchSerializer,
    DatabaseYearSerializer, ContainerTypeSerializer, ShipSerializer, PavilionSerializer
)
import json
import re


@ensure_csrf_cookie
def get_csrf_token(request):
    """Endpoint pentru obtinerea CSRF token"""
    return JsonResponse({'detail': 'CSRF cookie set'})


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint pentru autentificare JSON
    POST /api/login/
    Body: {"username": "...", "password": "..."}
    """
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'detail': 'Username și password sunt obligatorii'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({
                'detail': 'Autentificare reușită',
                'username': user.username
            })
        else:
            return Response(
                {'detail': 'Credențiale invalide'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        return Response(
            {'detail': f'Eroare la autentificare: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint pentru logout JSON
    POST /api/logout/
    """
    logout(request)
    return Response({'detail': 'Deconectare reușită'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth_view(request):
    """
    Endpoint pentru verificare autentificare
    GET /api/check-auth/
    """
    return Response({
        'authenticated': True,
        'username': request.user.username
    })


class ManifestEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pentru cautare si vizualizare intrari manifest.
    Doar utilizatorii autentificati pot accesa.
    """
    queryset = ManifestEntry.objects.select_related('container_type_rel', 'ship_rel', 'ship_rel__pavilion', 'database_year').all()
    serializer_class = ManifestEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numar_manifest', 'container', 'model_container', 'nume_nava']
    ordering_fields = ['data_inregistrare', 'created_at', 'numar_manifest']
    ordering = ['-data_inregistrare']

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Endpoint custom pentru cautare dupa container cu validare minim 7 cifre
        GET /api/manifests/search/?container=XXXX1234567&year=2025
        """
        serializer = ManifestSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        container = serializer.validated_data.get('container', '').strip()
        numar_manifest = serializer.validated_data.get('numar_manifest', '').strip()
        year = serializer.validated_data.get('year')

        # Validare: container trebuie sa contina minim 7 cifre
        if container:
            digits = re.findall(r'\d', container)
            if len(digits) < 7:
                return Response(
                    {'detail': 'Containerul trebuie să conțină minim 7 cifre'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        queryset = self.get_queryset()

        # Filtru dupa an
        if year:
            queryset = queryset.filter(database_year__year=year)
        else:
            # Daca nu e specificat anul, foloseste anul activ
            active_year = DatabaseYear.objects.filter(is_active=True).first()
            if active_year:
                queryset = queryset.filter(database_year=active_year)

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


class DatabaseYearViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pentru DatabaseYear - read only - accesibil fara autentificare"""
    queryset = DatabaseYear.objects.all()
    serializer_class = DatabaseYearSerializer
    permission_classes = [AllowAny]  # Permite acces fara autentificare
    ordering = ['-year']


class ContainerTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pentru ContainerType - read only"""
    queryset = ContainerType.objects.all()
    serializer_class = ContainerTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['model_container', 'tip_container']


class ShipViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pentru Ship - read only"""
    queryset = Ship.objects.select_related('pavilion').all()
    serializer_class = ShipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nume', 'linie_maritima']


class PavilionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pentru Pavilion - read only"""
    queryset = Pavilion.objects.all()
    serializer_class = PavilionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nume']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_manifest_view(request):
    """
    Endpoint pentru obtinerea ultimului manifest actualizat
    Returneaza numarul manifest cel mai mare si data cea mai recenta
    """
    year = request.GET.get('year')

    queryset = ManifestEntry.objects.all()

    # Filtru dupa an
    if year:
        try:
            year_obj = DatabaseYear.objects.get(year=int(year))
            queryset = queryset.filter(database_year=year_obj)
        except DatabaseYear.DoesNotExist:
            pass
    else:
        # Foloseste anul activ
        active_year = DatabaseYear.objects.filter(is_active=True).first()
        if active_year:
            queryset = queryset.filter(database_year=active_year)

    # Gaseste intrarea cu data_inregistrare cea mai recenta
    latest_entry = queryset.filter(
        data_inregistrare__isnull=False
    ).order_by('-data_inregistrare', '-numar_manifest').first()

    if latest_entry:
        return Response({
            'numar_manifest': latest_entry.numar_manifest,
            'data_inregistrare': latest_entry.data_inregistrare.strftime('%d.%m.%Y') if latest_entry.data_inregistrare else None,
            'nume_nava': latest_entry.nume_nava or None
        })
    else:
        return Response({
            'numar_manifest': None,
            'data_inregistrare': None,
            'nume_nava': None
        })
