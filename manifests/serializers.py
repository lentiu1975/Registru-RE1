from rest_framework import serializers
from .models import ManifestEntry, DatabaseYear, ContainerType, Ship, Pavilion


class DatabaseYearSerializer(serializers.ModelSerializer):
    """Serializer pentru DatabaseYear"""
    entries_count = serializers.IntegerField(source='entries.count', read_only=True)

    class Meta:
        model = DatabaseYear
        fields = ['id', 'year', 'is_active', 'entries_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class PavilionSerializer(serializers.ModelSerializer):
    """Serializer pentru Pavilion"""
    imagine_url = serializers.SerializerMethodField()

    class Meta:
        model = Pavilion
        fields = ['id', 'nume', 'nume_tara', 'imagine', 'imagine_url', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_imagine_url(self, obj):
        if obj.imagine:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagine.url)
            return obj.imagine.url
        return None


class ShipSerializer(serializers.ModelSerializer):
    """Serializer pentru Ship"""
    imagine_url = serializers.SerializerMethodField()
    pavilion_data = PavilionSerializer(source='pavilion', read_only=True)

    class Meta:
        model = Ship
        fields = ['id', 'nume', 'linie_maritima', 'pavilion', 'pavilion_data', 'imagine', 'imagine_url', 'descriere', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_imagine_url(self, obj):
        if obj.imagine:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagine.url)
            return obj.imagine.url
        return None


class ContainerTypeSerializer(serializers.ModelSerializer):
    """Serializer pentru ContainerType"""
    imagine_url = serializers.SerializerMethodField()

    class Meta:
        model = ContainerType
        fields = ['id', 'model_container', 'tip_container', 'imagine', 'imagine_url', 'descriere', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_imagine_url(self, obj):
        if obj.imagine:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagine.url)
            return obj.imagine.url
        return None


class ManifestEntrySerializer(serializers.ModelSerializer):
    """Serializer pentru ManifestEntry API cu imagini"""
    container_type_data = ContainerTypeSerializer(source='container_type_rel', read_only=True)
    ship_data = ShipSerializer(source='ship_rel', read_only=True)
    data_inregistrare_formatted = serializers.SerializerMethodField()

    class Meta:
        model = ManifestEntry
        fields = [
            'id',
            'database_year',
            'numar_curent',
            'numar_manifest',
            'numar_permis',
            'numar_pozitie',
            'cerere_operatiune',
            'data_inregistrare',
            'data_inregistrare_formatted',
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
            'container_type_data',
            'ship_data',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'numar_curent', 'model_container', 'created_at', 'updated_at']

    def get_data_inregistrare_formatted(self, obj):
        if obj.data_inregistrare:
            return obj.data_inregistrare.strftime('%d.%m.%Y')
        return None


class ManifestSearchSerializer(serializers.Serializer):
    """Serializer pentru cautare manifest"""
    container = serializers.CharField(required=False, allow_blank=True)
    numar_manifest = serializers.CharField(required=False, allow_blank=True)
    year = serializers.IntegerField(required=False)
