from rest_framework import serializers
from .models import ManifestEntry


class ManifestEntrySerializer(serializers.ModelSerializer):
    """Serializer pentru ManifestEntry API"""

    class Meta:
        model = ManifestEntry
        fields = [
            'id',
            'numar_curent',
            'numar_manifest',
            'numar_permis',
            'numar_pozitie',
            'cerere_operatiune',
            'data_inregistrare',
            'container',
            'numar_colete',
            'greutate_bruta',
            'descriere_marfa',
            'tip_operatiune',
            'nume_nava',
            'pavilion_nava',
            'numar_sumara',
            'tip_container',
            'linie_maritima',
            'model_container',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'numar_curent', 'model_container', 'created_at', 'updated_at']


class ManifestSearchSerializer(serializers.Serializer):
    """Serializer pentru cautare manifest"""
    container = serializers.CharField(required=False, allow_blank=True)
    numar_manifest = serializers.CharField(required=False, allow_blank=True)
